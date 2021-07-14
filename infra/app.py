from aws_cdk import core
from config import props
from stacks.application import ApplicationStack

APP_NAME = f'AwesomeApp-{props.get("environment")}'

app = core.App()

awesome_application = ApplicationStack(
    scope=app,
    id=f"ApplicationStack-{props.get('environment')}",
    props=props
)

app.synth()
