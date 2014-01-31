from common.constants import *

from common import battlechar
from common import boundint

# DAMAGE STUN KNOCKBACK ANGLE

class Hare(battlechar.BattleChar):
    def __init__(self, name="Unnamed Hare", inSuper=0):
        self.type = C_HARE
        self.name = name
        self.speciesName = "Hare"
        self.youIconHeight = 75
        self.blockFXPoints = [ (9, -35), (33, -32), (9, -35) ]
        self.hareEnergy = boundint.BoundInt(0, HARE_ENERGY_MAX, 0)
        self.prevEnergy = self.hareEnergy.value
        self.energyDelayTick = HARE_ENERGY_DELAY
        self.energy = self.hareEnergy
        super(Hare, self).__init__(850, 13)

        self.speciesDesc = ("A speedy light-assault unit specializing in" +
                            " close-range combat and acrobatic mobility." +
                            "  Can quickly change distance in combat to" +
                            " close in for an offensive rush or back off" +
                            " defensively as needed.")

        self.setSuperValue(inSuper)

    def beginBattle(self):
        super(Hare, self).beginBattle()
        self.hareEnergy.change(HARE_ENERGY_BATTLE_START)

    def update(self):
        super(Hare, self).update()

        if self.prevEnergy != self.hareEnergy.value:
            self.energyDelayTick = 0

        self.prevEnergy = self.hareEnergy.value

        if self.energyDelayTick < HARE_ENERGY_DELAY:
            self.energyDelayTick += 1
        else:
            self.hareEnergy.add(HARE_ENERGY_RECHARGE)
            self.prevEnergy = self.hareEnergy.value
