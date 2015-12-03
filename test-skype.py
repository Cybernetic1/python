import Skype4Py

skype = Skype4Py.Skype()

skype.Attach()

print "Your full name:", skype.CurrentUser.FullName
print "Your contacts:"
for user in skype.Friends:
	print "    ", user.FullName
