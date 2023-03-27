import whisper
import sys


def main(src):
    model = whisper.load_model('base')
    result = model.transcribe(src)
    print(result)


if __name__ == '__main__':
    main(sys.argv[1])
