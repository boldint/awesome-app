import os
from aws_cdk import (
    core,
    aws_iam as iam,
    aws_ecr_assets as ecr_assets,
    aws_apprunner as app_runner
)


class ApplicationStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, props: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ################################################################################################################
        # APP DOCKER IMAGE
        ################################################################################################################
        app_image = ecr_assets.DockerImageAsset(
            self,
            id="ApplicationDockerImage",
            directory=os.path.join(os.path.dirname(__file__), "..", "..", "app"),
            repository_name=f'awesome-app-{str(props.get("environment")).lower()}'
        )

        ################################################################################################################
        # ECR ROLE
        ################################################################################################################
        app_runner_ecr_role = iam.Role(
            scope=self,
            id=f"AppRunnerEcrRole-{props.get('environment')}",
            assumed_by=iam.ServicePrincipal("build.apprunner.amazonaws.com")
        )
        app_image.repository.grant_pull(app_runner_ecr_role)

        ################################################################################################################
        # APP-RUNNER SERVICE
        ################################################################################################################
        application = app_runner.CfnService(
            scope=self,
            id=f"AwesomeApp-{props.get('environment')}",
            source_configuration=app_runner.CfnService.SourceConfigurationProperty(
                authentication_configuration=app_runner.CfnService.AuthenticationConfigurationProperty(
                    access_role_arn=app_runner_ecr_role.role_arn
                ),
                image_repository=app_runner.CfnService.ImageRepositoryProperty(
                    image_identifier=app_image.image_uri,
                    image_repository_type="ECR",
                    image_configuration=app_runner.CfnService.ImageConfigurationProperty(
                        port="3000"
                    )
                )
            ),

            health_check_configuration=app_runner.CfnService.HealthCheckConfigurationProperty(
                path="/",
                healthy_threshold=3,
                unhealthy_threshold=3
            ),
            instance_configuration=app_runner.CfnService.InstanceConfigurationProperty(
                cpu="1024",
                memory="2048"
            )
        )




