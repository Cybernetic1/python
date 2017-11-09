import speech_recognition as sr

# List sound devices
for index, name in enumerate(sr.Microphone.list_microphone_names()):
	print("{1} index={0}".format(index, name))

r = sr.Recognizer()

with sr.AudioFile("test.flac") as source:

	print("Say something....")
	audio = r.record(source)

print("I'm here...")

r.dynamic_energy_threshold = False
print(r.energy_threshold)

result = None

try:
	result = r.recognize_google(audio, language = "yue-Hant-HK")
	# result = r.recognize_google(audio)
except sr.UnknownValueError:
	print("Could not understand you")
except sr.RequestError as e:
	print("Google error: {0}".format(e))


print(result)
exit(0)
