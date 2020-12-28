import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')


@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    question = event.message.text
    try:
        finder = Seacher()
        profile = line_bot_api.get_profile(event.source.user_id)
        annoy = random.choice(finder.searchArticle(question))
        str1 = "Hi "+ profile.display_name + " !\n\n"
        str2 = '\n\n You can click the link below\n' +annoy ['url']
        answer = qanet(question,annoy['content'])
        message = TextSendMessage(text= str1+ answer +str2)
        line_bot_api.reply_message(event.reply_token,message)

    except TypeError:
        message = TextSendMessage(text="can you type new query")
        line_bot_api.reply_message(event.reply_token,message)
    
import os 
if __name__ == "__main__":
    print("start line bot")
    context = ('ssl/fullchain.pem', 'ssl/privkey.pem')
    app.run(host='0.0.0.0', port= 5000, debug=True, ssl_context=context)