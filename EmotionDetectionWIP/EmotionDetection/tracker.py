import mysql.connector
from detector import Detector

conn = mysql.connector.connect(host='localhost', user='root', password='password2006', database='emotions')
cursor = conn.cursor()

print("Connection Established: " + str(conn.is_connected()))

def emotion_instances(emotions_):
    emotions = {'angry': 0, 'happy': 0, 'sad': 0, 'neutral': 0, 'disgust': 0, 'surprise': 0, 'fear': 0}

    for k in emotions_:
        if k.lower() == 'angry':
            emotions['angry'] += 1

        elif k.lower() == 'happy':
            emotions['happy'] += 1

        elif k.lower() == 'sad':
            emotions['sad'] += 1

        elif k.lower() == 'neutral':
            emotions['neutral'] += 1

        elif k.lower() == 'disgust':
            emotions['disgust'] += 1

        elif k.lower() == 'surprise':
            emotions['surprise'] += 1

        else:
            emotions['fear'] += 1

    min, max = emotions['angry'], emotions['angry']
    least_emotion, common_emotion = None, None

    for k in emotions:
        if emotions[k] < min:
            min, least_emotion = emotions[k], k

        if emotions[k] > max:
            max, common_emotion = emotions[k], k

    return least_emotion, common_emotion

while True:
    opt = int(input("1 - Record emotions, 2 - Retrieve user emotions, 3 - Quit: "))
    
    if opt == 1:
        user_id = input("U_id: ")

        time_offset = int(input("Enter time offset (Frequency at which data is recorded): "))
        assert(time_offset <= 100)
        detector = Detector('-c')

        emotions, avg_age, avg_angry_age = detector.capture_video(time_offset)
        min, max = emotion_instances(emotions)

        cursor.execute(f'insert into EmotionTracker values ("{user_id}", {avg_age}, {avg_angry_age}, "{max}", "{min}")')
        conn.commit()

    elif opt == 2:
        user_id = input("U_id: ")

        cursor.execute(f'select * from EmotionTracker where user_id={user_id}')

        for k in cursor.fetchall():
            print(k)
    
    else:
        break