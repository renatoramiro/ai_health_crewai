import os
from flask import Blueprint, jsonify, request
from crew.health_flow import HealthFlow
from evolutionapi.client import EvolutionClient
from evolutionapi.models.message import TextMessage
from db_helper import DatabaseHelper
from dotenv import load_dotenv
from datetime import datetime
import uuid

load_dotenv()

api_bp = Blueprint("api", __name__)

# Initialize WhatsApp client
whatsapp_client = EvolutionClient(
    base_url=os.getenv("EVOLUTION_BASE_URL"),
    api_token=os.getenv("EVOLUTION_API_TOKEN")
)
instances = whatsapp_client.instances.fetch_instances()

# Initialize DatabaseHelper
db = DatabaseHelper(
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432")
)

@api_bp.route("/webhook/agent_health", methods=["POST"])
def whatsapp_webhook():
    try:
        print("=== Iniciando processamento do webhook ===")
        # Get the webhook data
        webhook_data = request.get_json()
        print("Webhook data recebido:", webhook_data)
        
        # Check if webhook_data is a list or dict
        if isinstance(webhook_data, list):
            data = webhook_data[0]
        else:
            data = webhook_data

        # Extract message details from the webhook data structure
        if data.get('event') == 'messages.upsert':
            print("Evento messages.upsert detectado")
            message_data = data.get('data', {}).get('message', {})
            print("Message data:", message_data)
            
            # Extract conversation text - try both direct text and conversation
            message = (message_data.get('conversation', '') or 
                      message_data.get('text', '') or 
                      message_data.get('extendedTextMessage', {}).get('text', '')).strip()
            
            # Extract sender number from remoteJid
            sender = data.get('data', {}).get('key', {}).get('remoteJid', '')
            
            print(f"Mensagem extraída: '{message}', Sender: {sender}")
            
            if message and sender:
                result = None  # Initialize result variable
                
                # First, add current message to memory
                print("Adicionando mensagem atual ao banco...")
                try:
                    db.save_conversation({
                        'session_id': str(sender),
                        'role': 'user',
                        'message': str(message),
                        'created_at': datetime.now().isoformat(),
                        'sender': str(sender)
                    })
                    print("Mensagem adicionada ao banco com sucesso")
                except Exception as add_error:
                    print("Erro ao adicionar mensagem ao banco:", str(add_error))
                
                # Then get history and format it
                print("Buscando histórico no banco...")
                try:
                    conversations = db.get_conversations_by_session(str(sender))
                    history = []
                    if conversations:
                        for conv in conversations:
                            if conv['content'] and 'message' in conv['content']:
                                history.append(f"{conv['content']['role'].upper()}: {conv['content']['message']}")
                    history_text = "\n".join(history) if history else ""
                    print("Histórico formatado:", history_text)
                except Exception as search_error:
                    print("Erro ao buscar histórico:", str(search_error))
                    history_text = ""
                
                # Finally, process with HealthFlow
                try:
                    print("Iniciando processamento com HealthFlow...")
                    flow = HealthFlow()
                    flow.plot()
                    result = flow.run(message, history=history_text)
                    print("Resultado do HealthFlow:", result)
                except Exception as crew_error:
                    print('Erro no processamento do HealthFlow:', str(crew_error))
                
                if result:
                    print("Preparando resposta para WhatsApp...")
                    # Send response via WhatsApp
                    response_message = TextMessage(
                        number=sender,
                        text=str(result),
                        delay=2000
                    )
                    
                    try:
                        # Add the response to memory
                        print("Adicionando resposta ao banco...", result)
                        db.save_conversation({
                            'session_id': str(sender),
                            'role': 'assistant',
                            'message': str(result),
                            'created_at': datetime.now().isoformat(),
                            'sender': str(sender)
                        })
                        print("Resposta adicionada ao banco com sucesso")

                        # print("Enviando mensagem via WhatsApp...")
                        # response = whatsapp_client.messages.send_text(
                        #     os.getenv("EVOLUTION_INSTANCE"), 
                        #     response_message, 
                        #     os.getenv("EVOLUTION_INSTANCE_TOKEN")
                        # )
                        # print("Resposta do WhatsApp:", response)
                        
                        # return jsonify({
                        #     "status": "success",
                        #     "message": "Information was sent",
                        #     "sender": sender,
                        #     "received_message": message,
                        #     "response": result
                        # })
                    except Exception as error:
                        print("Erro ao processar resposta:", str(error))
                        return jsonify({
                            "status": "error",
                            "message": f"Error processing response: {str(error)}",
                            "sender": sender,
                            "received_message": message
                        }), 500
                else:
                    print("Nenhum resultado obtido do HealthFitnessCrew")
                    return jsonify({
                        "status": "error",
                        "message": "Failed to process information request",
                        "sender": sender,
                        "received_message": message
                    }), 500
        
        print("Evento não reconhecido ou ignorado")
        return jsonify({
            "status": "ignored",
            "message": "Not a valid message event",
            "event_type": data.get('event')
        })

    except Exception as e:
        print('Erro no webhook:', str(e))
        print('Tipo do erro:', type(e))
        import traceback
        print('Traceback:', traceback.format_exc())
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500