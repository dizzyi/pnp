from inovopy.robot import InovoRobot

def main():
    bot = InovoRobot.default_iva("192.168.1.114")
    bot.gipper_activate()


if __name__ == "__main__":
    main()
