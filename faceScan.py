import cv2
import cvzone
import time
import face_recognition as fr
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
appSettings = {'databaseURL': 'https://biometric-attendance-54301-default-rtdb.asia-southeast1.firebasedatabase.app/'}
my_app2 = firebase_admin.initialize_app(cred, appSettings, name='my_app2')

ref = db.reference('/', app= my_app2)
facedata_ref = ref.child('facedata')
attendance_ref = ref.child('attendance')


global faceFrame, enc
faceFrame = " "
def gen():
    global faceFrame, enc
    t_end = time.time() + 13
    t = time.time()
    t2 = time.time()
    t2_end = time.time() + 7
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    flag = 0
    bbox = 0,0,0,0
    c1 = (0, 255, 0)
    c2 = (0, 255, 0)
    while t < t_end:
        success, img = cap.read()
        img2 = img
        img = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img2 = cvzone.cornerRect(img2, bbox, rt = 0, colorR = c1, colorC = c2)

        if(t2 <= t2_end):     
            on_vid_text = "Starting in " + str(int(t2_end - t2)) + " seconds"
            cv2.putText(img2, on_vid_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_4)
        ret, buffer = cv2.imencode('.jpg', img2)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        if(t2 > t2_end):
            faceFrame = fr.face_locations(img)
            enc = fr.face_encodings(img, faceFrame)[0]
            t = time.time()
        t2 = time.time()


    
    cv2.destroyAllWindows()
    enc = list(enc)

def sendData(enroll, name, clas):
    global enc
    encDict = {}
    attendDict = {}
    encDict[enroll] = list(enc)
    attendDict[enroll] = {"name": name, "class": int(clas)}
    print(attendDict)
    facedata_ref.update(encDict)
    attendance_ref.update(attendDict)

# {'300105': [-0.128557488322258, 0.06370990723371506, 0.046385496854782104, -0.009649059735238552, -0.0243518128991127, -0.01904170587658882, -0.02985210530459881, -0.0800979807972908, 0.15242841839790344, -0.12592850625514984, 0.2515498697757721, -0.037533555179834366, -0.19646833837032318, -0.11924758553504944, 0.032089266926050186, 0.06968551874160767, -0.13983376324176788, -0.11969871819019318, -0.04995063692331314, -0.05786291882395744, 0.021061468869447708, -0.01512955967336893, 0.05789078027009964, 0.06793229281902313, -0.12072944641113281, -0.40134626626968384, -0.09549528360366821, -0.11499844491481781, 0.010194388218224049, -0.1230924054980278, 0.08165034651756287, 0.11655490100383759, -0.15911592543125153, -0.03213915973901749, -0.04529297351837158, 0.01688127964735031, -0.01246439479291439, 0.019017517566680908, 0.28761374950408936, -0.008430873975157738, -0.17160668969154358, -0.06386061757802963, 0.040310002863407135, 0.2845230996608734, 0.1790722757577896, -0.00012909469660371542, -0.013933135196566582, -0.058487556874752045, 0.08236434310674667, -0.21307243406772614, 0.08088766783475876, 0.18746677041053772, 0.10101992636919022, 0.05501363426446915, 0.05718325078487396, -0.042150311172008514, 0.0033270493149757385, 0.061151646077632904, -0.16379107534885406, 0.057330887764692307, -0.018303565680980682, -0.10574161261320114, -0.06245364248752594, 0.02638895995914936, 0.21556860208511353, 0.11358146369457245, -0.053872767835855484, -0.13306541740894318, 0.14205783605575562, -0.1434134840965271, -0.07836040109395981, 0.11712873727083206, -0.1416459083557129, -0.18197201192378998, -0.28435635566711426, 0.04912758618593216, 0.339144229888916, 0.0698329508304596, -0.1714005321264267, 0.08137022703886032, -0.08346378803253174, -0.10308029502630234, 0.0830911248922348, 0.12250177562236786, -0.08521467447280884, -0.04448799788951874, -0.01978735625743866, 0.0907554179430008, 0.16389504075050354, 0.003760220482945442, -0.096518374979496, 0.19982826709747314, 0.007099812850356102, 0.023540645837783813, 0.09137525409460068, 0.016798757016658783, -0.012295272201299667, -0.025324590504169464, -0.17278966307640076, -0.059038642793893814, 0.12311288714408875, -0.002032487653195858, -0.00424356572329998, 0.07596398890018463, -0.20199403166770935, 0.124337337911129, 0.03839294612407684, -0.04776903986930847, 0.09473076462745667, 0.02300075814127922, -0.11397119611501694, -0.08663360029459, 0.14931190013885498, -0.2342860996723175, 0.1816849410533905, 0.11501488089561462, 0.01975359581410885, 0.1437588632106781, 0.0782521516084671, 0.07344929128885269, 0.010159026831388474, -0.029720544815063477, -0.10109858214855194, 0.0018511827802285552, 0.11309748888015747, 0.0567091628909111, 0.0477723553776741, -0.02840929478406906]}