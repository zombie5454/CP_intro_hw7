from agent.base_agent import BaseAgent
import random
import pygame


class SearchAgent(BaseAgent):
    def __init__(self, color="black", rows_n=8, cols_n=8, width=600, height=600):
        BaseAgent.__init__(self, color=color)
        if self.color == "black":
            self.icon = -1
            self.other_icon = 1
        else:
            self.icon = 1
            self.other_icon = -1

    def _isValidPos(self, pos):             
        return pos >= 0 and pos < self.cols_n

    def _allDirections(self):
        return [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

    def _getIcon(self, row, col, obs):
        return obs[self.cols_n * row + col]

    def _handleCell(self, row, col, state, icon):
        if icon == self.other_icon:
            state[0] = True
            return True
        else:
            state[1] = True
            return False

    def _iterateCells(self, start, step, state, obs):
        col = start[0] + step[0]
        row = start[1] + step[1]
        state[0] = state[1] = False
        while self._isValidPos(col) and self._isValidPos(row):
            icon = self._getIcon(row, col, obs)
            if icon == 0:
                break
            if not self._handleCell(row, col, state, icon):
                break
            col += step[0]
            row += step[1]

    def _isValidMove(self, row, col, obs):
        for step in self._allDirections():
            """
            2-element list indicating state
            0: has other piece
            1: ends with self color
            """
            state = [False, False]
            self._iterateCells((col, row), step, state, obs)
            if state[0] == True and state[1] == True and self._getIcon(row, col, obs) == 0:
                return True
        return False

    def allValidMove(self, obs):
        res = list()
        for i in range(self.cols_n * self.rows_n):
            row = i // self.cols_n
            col = i % self.cols_n
            if self._isValidMove(row, col, obs):
                res.append((col, row))
        return res

    def step(self, reward, obs):
        print("Board:")
        for i in range(self.cols_n * self.rows_n):
            print("{0:2d}".format(obs[i]), end=" \n"[i % self.cols_n == self.cols_n - 1])
        print(self.allValidMove(obs))
        
        m_col, m_row = None, None
        largest_num = 0
        for x, y in self.allValidMove(obs):
            if (x == 0 or x == self.cols_n - 1) and (y == 0 or y == self.rows_n - 1):
                m_col, m_row = x, y 
                break
            if not m_col is None and (x <= 1 or x >= self.cols_n - 2) and (y <= 1 or y >= self.rows_n - 2):
                continue
            all_num = 0 
            for step in self._allDirections():
                col = x + step[0]
                row = y + step[1]
                d_num = 0
                while self._isValidPos(col) and self._isValidPos(row) and self._getIcon(row, col, obs) == self.other_icon:
                    d_num += 1
                    col += step[0]
                    row += step[1]
                if self._isValidPos(col) and self._isValidPos(row) and self._getIcon(row, col, obs) == self.icon:
                    all_num += d_num  
            if all_num > largest_num:
                largest_num = all_num
                m_col, m_row = x, y
        print(m_col, m_row)                
                

        
            

        return (self.col_offset + m_col * self.block_len, self.row_offset + m_row * self.block_len), pygame.USEREVENT
