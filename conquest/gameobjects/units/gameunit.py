from enum import Enum

import pygame
from util.window import Window
from util.colors import Colors

class GameUnit:

    """
    base class for a generic unit
    buildings have 0 speed for reasons

    :parameter unitinfo: the basic stats and info for the units
    :parameter sprite (Surface): the sprite of the unit, preferably pixel art
    :parameter team (Team()): what team this unit is on
    :parameter position (int[y, x]): the position of the unit on the board, with a reversed axis

    :var requiredBuilding: unitinfo of building required to build unit
    """

    def __init__(self, unitinfo, sprite, team, position):
        self.unitinfo = unitinfo
        self.name = unitinfo["name"]

        self.maxHealth = unitinfo["stats"][0]
        self.currentHealth = self.maxHealth
        self.attack = unitinfo["stats"][1]
        self.speed = unitinfo["stats"][2]
        self.currentSpeed = self.speed
        self.attacksPerTurn = unitinfo["stats"][3]
        self.availableAttacks = self.attacksPerTurn
        self.range = unitinfo["stats"][4]
        self.cost = unitinfo["stats"][5]

        self.unittype = unitinfo["type"]

        self.sprite = sprite
        self.spriteRect = sprite.get_rect()

        self.team = team

        self.position = position

        self.requiredBuilding = None


    def targetAction(self, targetunit):
        if targetunit.team.number != self.team.number and self.availableAttacks > 0:
            targetunit.takeDamage(self.attack)
            self.availableAttacks -= 1


    def onCreation(self):
        self.currentSpeed = 0
        self.availableAttacks = 0


    def onTurnStart(self):
        pass


    def onTurnEnd(self):
        pass


    def onDeath(self):
        pass

    """cool stuff"""
    def setHealth(self, health):
        self.currentHealth = health


    def healUnit(self, amount):
        self.currentHealth += amount
        if self.currentHealth > self.maxHealth:
            self.currentHealth = self.maxHealth


    def takeDamage(self, damage):
        self.currentHealth -= damage


    def resetSpeed(self):
        self.currentSpeed = self.speed


    def resetAttack(self):
        self.availableAttacks = self.attacksPerTurn

    """display stuff"""
    def displayUnit(self, tileRect):
        self.spriteRect.center = tileRect.center

        highlightSurface = pygame.Surface((self.spriteRect.width, self.spriteRect.height))
        highlightSurface = highlightSurface.convert_alpha(Window.SURFACE)
        highlightSurface.fill(Colors.teamcolors[self.team.color])
        Window.SURFACE.blit(highlightSurface, self.spriteRect.topleft)

        Window.SURFACE.blit(self.sprite, self.spriteRect)
        Window().displayText("Health: " + str(self.currentHealth) + "/" + str(self.maxHealth), tileRect.x + 5, tileRect.y + 5, 20)
        if self.unittype == UnitType.SOLDIER:
            Window().displayText("Speed: " + str(self.currentSpeed) + "/" + str(self.speed), tileRect.bottomleft[0] + 5, tileRect.bottomleft[1] - 15, 20)


class UnitType(Enum):

    SOLDIER = 1
    BUILDING = 2