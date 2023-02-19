from time import sleep

print("Searching for Panda...")
sleep(1)
print("Contacting Mojang for Panda Location")
sleep(1)

try:
    import pandas
    print("Panda Found")
    print("No. (Not allergic)")
except:
    print("Panda go wer?")