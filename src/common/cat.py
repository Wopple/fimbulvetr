from common.constants import *

from common import battlechar
from common import boundint

class Cat(battlechar.BattleChar):
    def __init__(self, name="Unnamed Cat", inSuper=0):
        self.type = CAT
        self.name = name
        self.speciesName = "Cat"
        self.youIconHeight = 80
        self.blockFXPoints = [ (9, -35), (33, -32), (9, -35) ]
        self.catEnergy = boundint.BoundInt(0, CAT_ENERGY_MAX, 0)
        self.prevEnergy = self.catEnergy.value
        self.energyDelayTick = CAT_ENERGY_DELAY
        self.energy = self.catEnergy
        super(Cat, self).__init__(1000, 15)
        self.initSpecMoves()
        self.bladeChargeHit = True

        self.speciesDesc = ("An all-around warrior that wields a blade" +
                            " enchanted with Galdr runes.  Capable of both" +
                            " melee and magical ranged attacks, and" +
                            " comfortable at many distances.  Requires time" +
                            " to charge their slowly-depleting energy" +
                            " in order to maintain strength.")

        self.setSuperValue(inSuper)

    def beginBattle(self):
        super(Cat, self).beginBattle()
        self.catEnergy.change(CAT_ENERGY_BATTLE_START)
        self.energyDelayTick = 0
        self.energyIsChangable = False

    def countdownComplete(self):
        self.energyIsChangable = True

    def update(self):
        super(Cat, self).update()
        
        hitCheck = False
        if (self.attackCanHit) and (not self.bladeChargeHit):
            self.bladeChargeHit = True
        elif (not self.attackCanHit) and (self.bladeChargeHit):
            self.bladeChargeHit = False
            hitCheck = True

        if self.energyIsChangable:
            if self.currMove.chargeBlade or hitCheck:
                self.catEnergy.add(CAT_ENERGY_RECHARGE)
                self.energyDelayTick = 0
            else:
                if self.energyDelayTick < CAT_ENERGY_DELAY:
                    self.energyDelayTick += 1
                else:
                    self.catEnergy.add(-CAT_ENERGY_USAGE)

    def getCatEnergyLevel(self):
        x = len(CAT_ENERGY_SECTIONS)

        for i in range(x):
            if self.energy.value <= CAT_ENERGY_SECTIONS[i]:
                return i+1

        return x+1
