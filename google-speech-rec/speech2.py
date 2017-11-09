import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone(device_index = 0) as source:
	print("Say something!")
	audio = r.record(source, duration = 5, offset = None)

try:
	print("You said " + r.recognize_google(audio, language = 'yue-Hant-HK'))
except sr.UnknownValueError:
	print("Could not understand you")
except sr.RequestError as e:
	print("Error {0}".format(e))

exit(0)


try:
	print(r.recognize_sphinx(audio, language = "yue-Hant-HK"))
except sr.UnknownValueError:
	print("Could not understand you")
except sr.RequestError as e:
	print("Error {0}".format(e))

exit(0)
