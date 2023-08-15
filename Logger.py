# flake8: noqa
from __future__ import annotations
import os
from pathlib import Path
from datetime import datetime
import logging
from logging import Formatter, handlers, getLogger, Handler
import inspect

from rich.logging import RichHandler


# logファイルの名前
LOG_FILE_NAME = f'app_{datetime.strftime(datetime.now(), "%Y%m%d")}.log'


class Logger:
    """
    Attributes
    ----------
    log_level : str
        追跡するログレベル, e.g. 'DEBUG' | 'INFO' | 'WARN' | 'ERROR'
    save_log_dir : Path
        ログを書き出すディレクトリ

    Methods
    -------
    debug
        debugレベルログを出力
    info
        infoレベルログを出力
    warn
        warnレベルログを出力
    error
        errorレベルログを出力
    remove_oldlog
        ログディレクトリにmax_log_num以上logファイルがある場合、最も古いlogファイルを消去
    """

    def __init__(
            self,
            *,
            log_level: str = 'INFO',
            save_log_dir: str = 'logs'):
        self.log_dir: Path = Path(save_log_dir)
        self.log_backupcount: int = 3
        if not os.path.exists(self.log_dir):  # logs/ディレクトリが無ければ作成
            os.makedirs(self.log_dir)
            self._create_log_gitignore()
        log_file_path: Path = self.log_dir/LOG_FILE_NAME

        stdout_formatter: Formatter = Formatter(fmt='%(message)s')
        file_formatter: Formatter = Formatter(
            fmt='%(asctime)s.%(msecs)03d %(levelname)7s %(message)s [%(name)s:%(lineno)d]',
            datefmt='%Y/%m/%d %H:%M:%S')

        stdout_handler: Handler = RichHandler(rich_tracebacks=True)
        stdout_handler.setFormatter(fmt=stdout_formatter)
        file_handler: Handler = handlers.RotatingFileHandler(
            filename=log_file_path,
            encoding='UTF-8',
            maxBytes=2**24,  # 16MB
            backupCount=self.log_backupcount)
        file_handler.setFormatter(fmt=file_formatter)

        logging.basicConfig(level=log_level, handlers=[
                            stdout_handler, file_handler])
        caller_func_name: str = inspect.stack(
        )[1].filename.split('/')[-1]  # 呼び出し元関数名
        self.logger = getLogger(name=caller_func_name)

    def debug(self, msg: str) -> None:
        self.logger.debug(msg, stacklevel=2)

    def info(self, msg: str) -> None:
        self.logger.info(msg, stacklevel=2)

    def warn(self, msg: str) -> None:
        self.logger.warning(msg, stacklevel=2)

    def error(self, msg: str, *, exc_info: bool = True) -> None:
        self.logger.error(msg, exc_info=exc_info, stacklevel=2)

    def critical(self, msg: str) -> None:
        self.logger.critical(msg, stacklevel=2)

    def remove_oldlog(self, *, max_num_log: int = 100) -> None:
        """ログディレクトリにmax_log_num以上logファイルがある場合、最も古いlogファイルを消去

        Parameters
        ----------
        max_log_num : int, optional
            logファイルの最大件数, by default 100
        """
        logs: list[str] = list(self.log_dir.glob('*.log'))
        if len(logs) > max_num_log:
            # log_name_pairs: [(logname_yyyymmdd.log, datetime(yyyy, mm, dd)), ...]
            log_name_pairs: list[tuple[str, datetime]] = [
                (log, datetime.strptime(log[-12:-4], '%Y%m%d')) for log in logs]
            log_name_pairs = sorted(log_name_pairs, key=lambda s: s[1])
            remove_log_path: str = log_name_pairs[0][0]  # 最も古いlogファイル
            os.remove(remove_log_path)
            self.info(f'remove {remove_log_path}')
            # ローテーションされたlogファイル (logname_yyyymmdd.log.1) 等がある場合、それらも削除する
            for i in range(1, self.log_backupcount+1):
                remove_rotating_log_path: str = remove_log_path + f'.{i}'
                if os.path.exists(remove_rotating_log_path):
                    os.remove(remove_rotating_log_path)
                    self.info(f'removed {remove_rotating_log_path}')

    def _create_log_gitignore(self) -> None:
        """logs/ ディレクトリに .gitignore を作成"""
        content: str = (
            '*\n'
            '!.gitignore\n'
        )
        with open(self.log_dir/'.gitignore', 'w') as f:
            f.write(content)

# いつも使わせていただいてます。ありがとうございます。
# 本家様:https://laid-back-scientist.com/log
