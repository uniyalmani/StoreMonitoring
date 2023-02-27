from kafka.admin import KafkaAdminClient, NewTopic


def create_topic(topic_name: str, num_partitions: int = 1, replication_factor: int=1):
    admin_client = KafkaAdminClient(
        bootstrap_servers='kafka:29092', 
        client_id='test'
    )

    try:
        topic_list = []
        print("creating topic")
        topic_list.append(NewTopic(name=topic_name, num_partitions=1, replication_factor=1))
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        print("topic created")
    except Exception as e:
        return {
            "error": e
        }