from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_iam as iam,
    aws_elasticloadbalancingv2 as elbv2,
    CfnOutput
)
import aws_cdk as cdk
from constructs import Construct


class HelloWorldEcsStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a VPC
        vpc = ec2.Vpc(self, "HelloWorldVpc", max_azs=3)

        # Create an ECS cluster
        cluster = ecs.Cluster(self, "HelloWorldCluster", vpc=vpc)

        # Define a Task Role
        task_role = iam.Role(self, "HelloWorldTaskRole",
                             assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"))

        # Define a Task Definition
        task_definition = ecs.FargateTaskDefinition(self, "HelloWorldTaskDef",
                                                    memory_limit_mib=512,
                                                    cpu=256,
                                                    task_role=task_role)

        # Add a container to the Task Definition
        container = task_definition.add_container("HelloWorldContainer",
                                                  image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                                                  logging=ecs.LogDriver.aws_logs(stream_prefix="HelloWorld"))

        # Map a port from the container to the host
        container.add_port_mappings(ecs.PortMapping(container_port=80))

        # Create a Fargate Service
        service = ecs.FargateService(self, "HelloWorldService",
                                     cluster=cluster,
                                     task_definition=task_definition,
                                     desired_count=1)

        # Create an Application Load Balancer
        lb = elbv2.ApplicationLoadBalancer(self, "HelloWorldLB", vpc=vpc, internet_facing=True)

        # Add a Listener to the Load Balancer
        listener = lb.add_listener("PublicListener", port=80, open=True)

        # Add a Target Group to the Listener
        listener.add_targets("ECS",
                             port=80,
                             targets=[service],
                             health_check=elbv2.HealthCheck(path="/", interval=cdk.Duration.minutes(1)))

        # Output the Load Balancer DNS Name
        CfnOutput(self, "LoadBalancerDNS", value=lb.load_balancer_dns_name)
