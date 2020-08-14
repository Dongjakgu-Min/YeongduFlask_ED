from email.mime.text import MIMEText
from tools.Email import smtp


def send_mail(to, board_name, title):
    msg = MIMEText('새로운 {0} 게시물이 올라왔습니다. \n'
                   '제목 : {1}'.format(board_name, title))
    msg['Subject'] = 'NCLab 게시물 알리미 - 새로운 게시글이 올라왔습니다.'
    msg['To'] = to
    smtp.sendmail('Yeongdu Land', to, msg.as_string())
