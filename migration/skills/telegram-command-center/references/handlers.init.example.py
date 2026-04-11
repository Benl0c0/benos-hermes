"""Register command handlers in COMMANDS dict"""

from .help_cmd import handle_help
# from .usage_cmd import handle_usage
# from .logs_cmd import handle_logs
# from .model_cmd import handle_model
# from .restart_cmd import handle_restart
# from .health_cmd import handle_health
# from .selfdestruct_cmd import handle_selfdestruct

COMMANDS = {
    'help': handle_help,
    # 'usage': handle_usage,
    # 'logs': handle_logs,
    # 'model': handle_model,
    # 'restart': handle_restart,
    # 'health': handle_health,
    # 'selfdestruct': handle_selfdestruct,
}
