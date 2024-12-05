import os
from flask import Blueprint, jsonify, request
from crew import HealthFitnessCrew
from evolutionapi.client import EvolutionClient
from evolutionapi.models.message import TextMessage
from mem0 import Memory
from dotenv import load_dotenv

load_dotenv()

api_bp = Blueprint("api", __name__)

# Initialize WhatsApp client
whatsapp_client = EvolutionClient(
    base_url=os.getenv("EVOLUTION_BASE_URL"),
    api_token=os.getenv("EVOLUTION_API_TOKEN")
)
instances = whatsapp_client.instances.fetch_instances()

config_pgvector = {
    "vector_store": {
        "provider": "pgvector",
        "version": "v1.1",
        "config": {
            "dbname": os.getenv("POSTGRES_DB"),
            "collection_name": os.getenv("POSTGRES_COLLECTION_NAME"),
            "embedding_model_dims": 1536,
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "host": os.getenv("POSTGRES_HOST"),
            "port": os.getenv("POSTGRES_PORT"),
            "diskann": False
        }
    }
}

memory = Memory.from_config(config_pgvector)

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
                print("Adicionando mensagem atual à memória...")
                try:
                    result_added = memory.add(message, user_id=str(sender), metadata={"data": "info"})
                    print("Mensagem adicionada à memória:", result_added)
                except Exception as add_error:
                    print("Erro ao adicionar mensagem à memória:", str(add_error))
                
                # Then get history and format it
                print("Buscando histórico na memória...")
                try:
                    search_results = memory.search(message, user_id=str(sender), limit=20)
                    print("Resultados da busca:", search_results)
                    history = []
                    if search_results:
                        for item in search_results:
                            if isinstance(item, dict) and 'memory' in item:
                                history.append(item['memory'])
                    history_text = "\n".join(history) if history else ""
                    print("Histórico formatado:", history_text)
                except Exception as search_error:
                    print("Erro ao buscar histórico:", str(search_error))
                    history_text = ""
                
                # Finally, process with HealthFitnessCrew
                try:
                    print("Iniciando processamento com HealthFitnessCrew...")
                    crew = HealthFitnessCrew()
                    result = crew.run(message, history=history_text)
                    print("Resultado do HealthFitnessCrew:", result)
                except Exception as crew_error:
                    print('Erro no processamento do HealthFitnessCrew:', str(crew_error))
                
                if result:
                    print("Preparando resposta para WhatsApp...")
                    # Send response via WhatsApp
                    response_message = TextMessage(
                        number=sender,
                        text=str(result),
                        delay=2000
                    )
                    
                    try:
                        print("Enviando mensagem via WhatsApp...")
                        response = whatsapp_client.messages.send_text(
                            os.getenv("EVOLUTION_INSTANCE"), 
                            response_message, 
                            os.getenv("EVOLUTION_INSTANCE_TOKEN")
                        )
                        print("Resposta do WhatsApp:", response)
                        
                        # Add the response to memory
                        print("Adicionando resposta à memória...")
                        memory.add(str(result), user_id=str(sender), metadata={"data": "info"})
                        
                        return jsonify({
                            "status": "success",
                            "message": "Information was sent",
                            "sender": sender,
                            "received_message": message
                        })
                    except Exception as whatsapp_error:
                        print("Erro ao enviar mensagem WhatsApp:", str(whatsapp_error))
                        raise
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