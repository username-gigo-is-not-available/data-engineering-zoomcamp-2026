from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment


def create_source(t_env):
    table_name = "green_trips"
    t_env.execute_sql(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            PULocationID        INTEGER,
            DOLocationID        INTEGER,
            passenger_count     INTEGER,
            trip_distance       DOUBLE,
            tip_amount          DOUBLE,
            total_amount        DOUBLE,
            lpep_pickup_datetime  VARCHAR,
            lpep_dropoff_datetime VARCHAR,
            event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'topic' = 'green-trips',
            'scan.startup.mode' = 'earliest-offset',
            'properties.auto.offset.reset' = 'earliest',
            'format' = 'json'
        )
    """)
    return table_name


def create_sink(t_env):
    table_name = "tumbling_window_largest_tip"
    t_env.execute_sql(f"""
                      CREATE TABLE IF NOT EXISTS {table_name}
                      (
                          window_start TIMESTAMP(3),
                          total_tip DOUBLE,
                          PRIMARY KEY (window_start) NOT ENFORCED
                      ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = {table_name},
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        )
                      """)
    return table_name


def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10 * 1000)
    env.set_parallelism(1)

    t_env = StreamTableEnvironment.create(
        env,
        environment_settings=EnvironmentSettings.new_instance().in_streaming_mode().build()
    )

    try:
        source = create_source(t_env)
        sink = create_sink(t_env)

        t_env.execute_sql(F"""
                          INSERT INTO {sink}
                          SELECT window_start,
                                 SUM(tip_amount) AS total_tip
                          FROM TABLE(
                                  TUMBLE(TABLE {source}, DESCRIPTOR(event_timestamp), INTERVAL '1' HOUR)
                               )
                          GROUP BY window_start
                          """).wait()

    except Exception as e:
        print("Job failed:", e)


if __name__ == "__main__":
    main()
