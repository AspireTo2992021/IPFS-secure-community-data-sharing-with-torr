from flask import Flask, jsonify, request , render_template , redirect , url_for
r = {'index': 4, 'message': 'Congratulations, you just mined a block!', 'previous_hash': '1886453d57b1d2000f7735c380cc337e71db46a58a58db5a342ee2f231b299c9', 'proof': 21391, 'timestamp': '2022-11-26 14:03:03.810544', 'transactions': [{'input': [{'amount': 1, 'receiver': 'candidate 1'}, {'amount': 0, 'sender': "b'5tYzQcQ32AJU4gagGoEGnXUtbkF48GJiwTq69YvJb9qfWh8RuHE4sJB'"}], 'output': [{'current_balance': 1, 'sender': "b'5tYzQcQ32AJU4gagGoEGnXUtbkF48GJiwTq69YvJb9qfWh8RuHE4sJB'"}]}]}


block_number = r["index"]

prev_hash = r["previous_hash"]
nonce = r["proof"]
timestamp =  r["timestamp"]

#'transactions': [{'input': [{'amount': 1, 'receiver': 'candidate 1'}, {'amount': 0, 'sender': ""}], 'output': [{'current_balance': 1, 'sender': ""}]}
transaction = r["transactions"]
input  = transaction[0]["output"]
output = transaction[0]["input"]

output_sender_dict = input[0]

input_receiver_dict = output[1]
input_sender_dict = output[0]

#print(f'{ block_number} , {prev_hash} , {nonce} , {timestamp} , {input_receiver_dict} , {output_sender_dict} , {input_sender_dict}')


print(f' keys  : {"code" in r.keys()}' )
app = Flask(__name__)
print(app.config)

@app.route("/")
def home():
    #return render_template("upload.html", name=filename, image1=filename, uploaded=True, img=True, result=result, audio=True, audio_text=audio_text,
                                   #audiofile=audiofile)
    
    return render_template('info_table.html' , block_number=block_number , prev_hash=prev_hash , nonce=nonce ,timestamp=timestamp,output_sender_dict=output_sender_dict ,input_receiver_dict1=input_receiver_dict ,input_sender_dict1=input_sender_dict)



app.debug = True
app.run('0.0.0.0',3001)
