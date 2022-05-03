from pydub import AudioSegment
from pydub.playback import play

audio1 = AudioSegment.from_file("A note.wav") #your first audio file
audio2 = AudioSegment.from_file("E minor chord.wav") #your second audio file
#audio3 = AudioSegment.from_file("chunk3.wav") #your third audio file

mixed = audio1.overlay(audio2)          #combine , superimpose audio files
#mixed1  = mixed.overlay(audio3)          #Further combine , superimpose audio files
#If you need to save mixed file
mixed.export("mixed.wav", format='wav') #export mixed  audio file
play(mixed)       