import winsound

def play_sound():
    winsound.PlaySound('sound.wav', winsound.SND_FILENAME)


def main():
    play_sound()
    play_sound()
    play_sound()

if __name__ == '__main__':
    main()
 



