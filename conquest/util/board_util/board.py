import pygame

from util.colors import Colors
from util.constants import Constants
from util.window import Window
from util.board_util.tile import Tile

class Board:

    """
    The amazing board
    So many methods
    whatever

    :var unitlist (GameObject[]): just a list of the units
    :var previousSelection (Tile): the selected tile that remains selected after a new tile is selected
    """

    boardtiles = []
    unitlist = []

    unitmoves = []
    unitattacks = []

    buildmoves = []

    topBorder = 0
    bottomBorder = 0
    leftBorder = 0
    rightBorder = 0

    previousSelection = None
    currentSelection = None

    selectedUnit = None

    '''util functions'''

    def generateBoard(self):
        self.boardtiles = []
        self.unitlist = []
        for i in range(0, Constants.BOARD_HEIGHT):
            self.boardtiles.append([])

        heightpixel = Constants.TOP_MARGIN_SIZE
        widthpixel = Constants.LEFT_MARGIN_SIZE

        for height in range(0, Constants.BOARD_HEIGHT):
            for width in range(0, Constants.BOARD_WIDTH):
                self.boardtiles[height].append(Tile(widthpixel, heightpixel, [height, width]))
                widthpixel += Constants.TILE_SIZE
            widthpixel = Constants.LEFT_MARGIN_SIZE
            heightpixel += Constants.TILE_SIZE

        self.leftBorder = self.boardtiles[0][0].rect.left
        self.topBorder = self.boardtiles[0][0].rect.top
        self.rightBorder = self.boardtiles[Constants.BOARD_HEIGHT - 1][Constants.BOARD_WIDTH - 1].rect.right
        self.bottomBorder = self.boardtiles[Constants.BOARD_HEIGHT - 1][Constants.BOARD_WIDTH - 1].rect.bottom


    # actually gets what you click
    def getTileSelection(self, mousepressed, mouseposition):
        if mousepressed:
            for height in range(0, len(self.boardtiles)):
                for width in range(0, len(self.boardtiles[0])):
                    if self.boardtiles[height][width].isHovered(mouseposition):
                        self.removeTileSelection()

                        if self.previousSelection is None:
                            self.previousSelection = self.boardtiles[height][width]
                            #self.removeTileSelection()
                        else:
                            self.clearMoves()
                            self.previousSelection = self.currentSelection
                        self.selectedUnit = self.getUnit(self.previousSelection)
                        self.currentSelection = self.boardtiles[height][width]
                        self.currentSelection.selected = True
                        return

            self.previousSelection = None
            self.currentSelection = None
            self.removeTileSelection()
            self.clearMoves()


    # just one tile
    def getSelectedTile(self):
        for height in range(0, len(self.boardtiles)):
            for width in range(0, len(self.boardtiles[0])):
                if self.boardtiles[height][width].selected:
                    return self.boardtiles[height][width]
        return None


    def removeTileSelection(self):
        for height in range(0, len(self.boardtiles)):
            for width in range(0, len(self.boardtiles[0])):
                self.boardtiles[height][width].selected = False


    def getAdjacentTiles(self, tilepos, distance):
        adjacent = []
        for i in range(1, distance + 1):
            if tilepos[0] + i < Constants.BOARD_HEIGHT:
                adjacent.append([tilepos[0] + i, tilepos[1]])
            if tilepos[0] - i >= 0:
                adjacent.append([tilepos[0] - i, tilepos[1]])
            if tilepos[1] + i < Constants.BOARD_WIDTH:
                adjacent.append([tilepos[0], tilepos[1] + i])
            if tilepos[1] - i >= 0:
                adjacent.append([tilepos[0], tilepos[1] - i])

        return adjacent


    def getTileDistance(self, tile1, tile2):
        tile1pos = tile1.position
        tile2pos = tile2.position
        return abs(tile2pos[0]-tile1pos[0]) + abs(tile2pos[1]-tile1pos[1])


    '''unit functions'''
    def addUnit(self, unit):
        self.unitlist.append(unit)


    def removeUnit(self, unit):
        self.unitlist.remove(unit)


    def moveUnit(self, unit, targettile):
        if targettile.position in self.unitmoves:
            unit.currentSpeed -= (abs(targettile.position[0] - unit.position[0]) + abs(targettile.position[1] - unit.position[1]))
            unit.position = [targettile.position[0], targettile.position[1]]
        self.selectedUnit = None
        self.removeTileSelection()
        self.clearMoves()
        self.currentSelection = None
        self.previousSelection = None


    def unitAction(self, unit, targettile):
        if targettile.position in self.unitattacks and targettile.position != unit.position:
            self.unitTargetAction(unit, self.getUnit(targettile))
            self.clearMoves()

            movetiles = self.getAdjacentTiles(targettile.position, unit.range)
            if unit.position in movetiles:
                return
            for tilepos in reversed(movetiles):
                if tilepos in self.unitmoves:
                    self.moveUnit(unit, self.boardtiles[tilepos[0]][tilepos[1]])
                    return


    def unitTargetAction(self, selectedunit, targetunit):
        if targetunit is not None and selectedunit is not targetunit:
            selectedunit.targetAction(targetunit)


    def killUnits(self):
        for i in self.unitlist:
            if i.currentHealth <= 0:
                i.onDeath()
                self.unitlist.remove(i)


    def resetUnitActions(self):
        for i in self.unitlist:
            i.resetSpeed()
            i.resetAttack()


    def getUnit(self, tile):
        for unit in self.unitlist:
            if unit.position == tile.position:
                return unit
        return None


    def tileOccupied(self, tile):
        if tile is None:
            return False
        if self.getUnit(tile) is None:
            return False
        return True


    def clearMoves(self):
        self.unitmoves = []
        self.unitattacks = []


    # UNIT MOVES AND ACTIONS
    def getUnitMoves(self, unit, tilepos, availablemoves):
        if tilepos in self.unitmoves:
            self.unitmoves.remove(tilepos)
        if self.tileOccupied(self.boardtiles[tilepos[0]][tilepos[1]]) and tilepos != unit.position:
            pass
        else:
            self.unitmoves.append(tilepos)
        if availablemoves == 0:
            return


        availablemoves -= 1

        if tilepos[0] + 1 < Constants.BOARD_HEIGHT:
            self.getUnitMoves(unit, [tilepos[0] + 1, tilepos[1]], availablemoves)
        if tilepos[0] - 1 >= 0:
            self.getUnitMoves(unit, [tilepos[0] - 1, tilepos[1]], availablemoves)
        if tilepos[1] + 1 < Constants.BOARD_WIDTH:
            self.getUnitMoves(unit, [tilepos[0], tilepos[1] + 1], availablemoves)
        if tilepos[1] - 1 >= 0:
            self.getUnitMoves(unit, [tilepos[0], tilepos[1] - 1], availablemoves)


    def getUnitAttacks(self, unit, tilepos, availableattacks):
        if tilepos in self.unitattacks:
            self.unitattacks.remove(tilepos)
        self.unitattacks.append(tilepos)
        if availableattacks == 0:
            return

        availableattacks -= 1

        if tilepos[0] + 1 < Constants.BOARD_HEIGHT:
            self.getUnitAttacks(unit, [tilepos[0] + 1, tilepos[1]], availableattacks)
        if tilepos[0] - 1 >= 0:
            self.getUnitAttacks(unit, [tilepos[0] - 1, tilepos[1]], availableattacks)
        if tilepos[1] + 1 < Constants.BOARD_WIDTH:
            self.getUnitAttacks(unit, [tilepos[0], tilepos[1] + 1], availableattacks)
        if tilepos[1] - 1 >= 0:
            self.getUnitAttacks(unit, [tilepos[0], tilepos[1] - 1], availableattacks)

    # called in eventhandler
    def getBuildMoves(self, buildinglist):
        self.buildmoves = []
        for building in buildinglist:
            poslist = self.getAdjacentTiles(building.position, 1)
            for pos in poslist:
                if not self.tileOccupied(self.boardtiles[pos[0]][pos[1]]):
                    if pos not in self.buildmoves:
                        self.buildmoves.append(pos)


    '''event functions'''

    def update(self, mousepressed, mouseposition, team):
        self.getTileSelection(mousepressed, mouseposition)

        if self.tileOccupied(self.previousSelection):
            if self.selectedUnit is not None:
                if self.selectedUnit.team.number == team.number:
                    if mousepressed:
                        self.getUnitMoves(self.selectedUnit, self.selectedUnit.position, self.selectedUnit.currentSpeed)
                        if self.selectedUnit.availableAttacks > 0:
                            self.getUnitAttacks(self.selectedUnit, self.selectedUnit.position, self.selectedUnit.range)

                    if not self.tileOccupied(self.currentSelection):
                        if self.currentSelection.position in self.unitmoves:
                            self.moveUnit(self.selectedUnit, self.currentSelection)
                    else:
                        if self.currentSelection.position in self.unitattacks:
                            self.unitAction(self.selectedUnit, self.currentSelection)
                    self.getBuildMoves(team.getBuildings())

        self.killUnits()


    '''display functions'''

    def displayUnits(self):
        for i in range(0, len(self.unitlist)):
            unitposition = self.unitlist[i].position
            self.unitlist[i].displayUnit(self.boardtiles[unitposition[0]][unitposition[1]].rect)


    def displayUnitMoves(self):
        for move in self.unitmoves:
            self.boardtiles[move[0]][move[1]].highlight("transparentlightblue")
        for attack in self.unitattacks:
            self.boardtiles[attack[0]][attack[1]].highlight("transparentred")


    def displayBoard(self, window, mousepos, interface):
        for height in range(0, len(self.boardtiles)):
            for width in range(0, len(self.boardtiles[0])):
                self.boardtiles[height][width].displayTile()
                pygame.draw.rect(Window.SURFACE, Colors.colorlist['black'], self.boardtiles[height][width].rect, 1)

        if mousepos[0] > self.leftBorder and mousepos[1] > self.topBorder:
            selectWidth = int((mousepos[0] - self.leftBorder) / Constants.TILE_SIZE)
            selectHeight = int((mousepos[1] - self.topBorder) / Constants.TILE_SIZE)
            if selectWidth >= 0 and selectWidth < Constants.BOARD_WIDTH and selectHeight >= 0 and selectHeight < Constants.BOARD_HEIGHT:
                self.boardtiles[selectHeight][selectWidth].highlight("transparentblue")
                unit = self.getUnit(self.boardtiles[selectHeight][selectWidth])
                if unit is not None:
                    interface.displayUnitInfo(window, unit.unitinfo, unit.position, unit.team)

        for move in self.buildmoves:
            self.boardtiles[move[0]][move[1]].highlight('transparentturqoise')

        self.displayUnitMoves()
        self.displayUnits()