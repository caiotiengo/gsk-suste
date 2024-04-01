css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.css-pxxe24 {
visibility: hidden;
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
 .stTextArea {
      position: fixed !important;
      bottom: 0rem !important;
      z-index: 100000  !important;
      padding-bottom: 62px  !important;
      background: #0e1117  !important;

    }
 .st-emotion-cache-19rxjzo ef3psqc7 {
        position: fixed !important;
        bottom: 1rem !important;
 }
 .st-emotion-cache-1xw8zd0{
    border: 0  !important;
 }
 .st-emotion-cache-19rxjzo ef3psqc7{
    position: fixed  !important;
    bottom: 12px  !important;
 }
 .css-1p05t8e{
     border: 0  !important;
 }
 .css-1q8dd3e {
    position: fixed !important;
    bottom: 20px !important;
    z-index: 1000000 !important;
 }
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://99prod.s3.amazonaws.com/uploads/8fc44766-d490-47b0-9792-b9aeff8848dd/598927_541420932593531_1192935286_n.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://cdn-icons-png.flaticon.com/512/3177/3177440.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''