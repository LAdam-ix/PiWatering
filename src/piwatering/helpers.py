def create_buckets(client, components, retention_days=None):
    buckets_api = client.buckets_api()

    for component_name in components:
        bucket_name = component_name.replace(" ", "_")
        existing_buckets = buckets_api.find_buckets(name=bucket_name).buckets
        if not existing_buckets:
            buckets_api.create_bucket(
                bucket_name=bucket_name,
            )
            print(f"Bucket '{bucket_name}' created.")
        else:
           print(f"Bucket '{bucket_name}' already exists.")




