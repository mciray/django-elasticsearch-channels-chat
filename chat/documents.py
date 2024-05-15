from django_elasticsearch_dsl import Document, Index
from django_elasticsearch_dsl.registries import registry
from .models import Message

@registry.register_document
class MessageDocument(Document):
    class Index:
        name = 'messages'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Message
        fields = [
            'content',
            'timestamp',  # timestamp alanını da ekleyin
        ]
