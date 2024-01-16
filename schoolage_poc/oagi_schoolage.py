import os

import google.generativeai as genai
from google.ai import generativelanguage as glm


oom_prompt = """What is the probability of retrying below operation resolve the issue ? please answer in json.
Do not include any explanations, only provide a  RFC8259 compliant JSON response  following this format without deviation:
{"retry": probability in float}
Error:
env: prod
job name: update_ny_taxi_data
ERROR Executor: Exception in task 7.0 in stage 6.0 (TID 439)
java.lang.OutOfMemoryError
    at java.io.ByteArrayOutputStream.hugeCapacity(Unknown Source)
    at java.io.ByteArrayOutputStream.grow(Unknown Source)
    at java.io.ByteArrayOutputStream.ensureCapacity(Unknown Source)
    at java.io.ByteArrayOutputStream.write(Unknown Source)
    at java.io.ObjectOutputStream$BlockDataOutputStream.drain(Unknown Source)
    at java.io.ObjectOutputStream$BlockDataOutputStream.setBlockDataMode(Unknown Source)
    at java.io.ObjectOutputStream.writeObject0(Unknown Source)
    at java.io.ObjectOutputStream.writeObject(Unknown Source)
    at org.apache.spark.serializer.JavaSerializationStream.writeObject(JavaSerializer.scala:44)
    at org.apache.spark.serializer.JavaSerializerInstance.serialize(JavaSerializer.scala:101)
    at org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:239)
    at java.util.concurrent.ThreadPoolExecutor.runWorker(Unknown Source)
    at java.util.concurrent.ThreadPoolExecutor$Worker.run(Unknown Source)
    at java.lang.Thread.run(Unknown Source)
"""

spark_network_timeout_prompt = """What is the probability of retrying below operation resolve the issue ? please answer in json.
Do not include any explanations, only provide a  RFC8259 compliant JSON response  following this format without deviation:
Error:
env: prod
job name: update_ny_taxi_data_network
ERROR Executor: Exception in task 7.0 in stage 6.0 (TID 439)
17/08/15 12:29:40 ERROR TransportChannelHandler: Connection to /192.168.xx.109:44271 has been quiet for 120000 ms while there are outstanding requests. Assuming connection is dead; please adjust spark.network.timeout if this is wrong.
17/08/15 12:29:40 WARN NettyRpcEndpointRef: Error sending message [message = RetrieveSparkProps] in 1 attempts
org.apache.spark.rpc.RpcTimeoutException: Futures timed out after [120 seconds]. This timeout is controlled by spark.rpc.askTimeout
	at org.apache.spark.rpc.RpcTimeout.org$apache$spark$rpc$RpcTimeout$$createRpcTimeoutException(RpcTimeout.scala:48)
	at org.apache.spark.rpc.RpcTimeout$$anonfun$addMessageIfTimeout$1.applyOrElse(RpcTimeout.scala:63)
	at org.apache.spark.rpc.RpcTimeout$$anonfun$addMessageIfTimeout$1.applyOrElse(RpcTimeout.scala:59)
	at scala.runtime.AbstractPartialFunction.apply(AbstractPartialFunction.scala:33)
	at org.apache.spark.rpc.RpcTimeout.awaitResult(RpcTimeout.scala:76)
	at org.apache.spark.rpc.RpcEndpointRef.askWithRetry(RpcEndpointRef.scala:101)
	at org.apache.spark.rpc.RpcEndpointRef.askWithRetry(RpcEndpointRef.scala:77)
	at org.apache.spark.executor.CoarseGrainedExecutorBackend$$anonfun$run$1.apply$mcV$sp(CoarseGrainedExecutorBackend.scala:172)
	at org.apache.spark.deploy.SparkHadoopUtil$$anon$1.run(SparkHadoopUtil.scala:68)
	at org.apache.spark.deploy.SparkHadoopUtil$$anon$1.run(SparkHadoopUtil.scala:67)
	at java.security.AccessController.doPrivileged(Native Method)
	at javax.security.auth.Subject.doAs(Subject.java:422)
"""

spark_oom_func = glm.FunctionDeclaration(
    name="spark_oom_func",
    description="Retry out of memory error of the spark job",
    parameters=glm.Schema(
        type=glm.Type.OBJECT,
        properties={
                'job': glm.Schema(type=glm.Type.STRING),
                'env': glm.Schema(type=glm.Type.STRING),
                'retry': glm.Schema(type=glm.Type.NUMBER)
        },
        required=[
            "retry",
            "job",
            "env"
        ],
    )
)

spark_network_timeout_func = glm.FunctionDeclaration(
    name="spark_network_timeout_func",
    description="Retry spark job network timeout error",
    parameters=glm.Schema(
        type=glm.Type.OBJECT,
        properties={
                'job': glm.Schema(type=glm.Type.STRING),
                'env': glm.Schema(type=glm.Type.STRING),
                'retry': glm.Schema(type=glm.Type.NUMBER)
        },
        required=[
            "retry",
            "job",
            "env"
        ],
    )
)

retry_func = glm.FunctionDeclaration(
    name="retry_func",
    description="Retry probability",
    parameters=glm.Schema(
        type=glm.Type.OBJECT,
        properties={
                'retry': glm.Schema(type=glm.Type.NUMBER)
        },
        required=[
            "retry",
        ],
    )
)

automation_tool = glm.Tool(
    function_declarations=[spark_oom_func,
                           spark_network_timeout_func,
                           retry_func],
)

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro', tools=[automation_tool])


response = model.generate_content(spark_network_timeout_prompt,
                                  generation_config=genai.types.GenerationConfig(
                                      temperature=0.0),
                                  )

model.generate_content
try:
    print(response.candidates)
except Exception as e:
    print(f'{type(e).__name__}: {e}')
