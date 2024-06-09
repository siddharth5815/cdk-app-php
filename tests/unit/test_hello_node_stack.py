import aws_cdk as core
import aws_cdk.assertions as assertions

from hello_node.hello_node_stack import HelloNodeStack

# example tests. To run these tests, uncomment this file along with the example
# resource in hello_node/hello_node_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = HelloNodeStack(app, "hello-node")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
