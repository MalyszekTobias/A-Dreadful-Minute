from app.game import Game
import sys
import asyncio

QX = Game()

if __name__ == '__main__':
    asyncio.run(QX.mainloop())