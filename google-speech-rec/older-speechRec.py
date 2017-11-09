import speech_recognition as sr

rec = Recorder(channels = 2)

AUDIO_FILE = "test.flac"

r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
	print("Say something!")
	audio = r.record(source)


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
