# solution and implementation
# Author : Colin Roskos
#

from PIMotors import Motor
from RubicksCube import RubiksCube
from RubicksCube import RubiksFace as RF
import Solver

def main():
    # define cube
    face_0 = RF(0, [0,0,0,0,0,0,0,0])
    face_1 = RF(1, [3,4,2,1,1,1,1,1])
    face_2 = RF(2, [1,2,2,1,2,4,2,2])
    face_3 = RF(3, [3,3,1,3,2,3,3,4])
    face_4 = RF(4, [4,4,4,4,4,5,3,5])
    face_5 = RF(5, [2,5,3,5,5,5,5,5])
    cube = RubiksCube(face_0,face_1,face_2,face_3,face_4,face_5)
   
    face_0 = RF(0, [0,0,0,0,0,0,0,0])
    face_1 = RF(1, [4,4,5,2,5,1,1,1])
    face_2 = RF(2, [5,5,2,2,2,5,5,2])
    face_3 = RF(3, [3,3,3,3,3,3,4,3])
    face_4 = RF(4, [4,4,4,1,3,1,4,5])
    face_5 = RF(5, [2,2,1,1,1,2,5,4])

    cube = RubiksCube(face_0,face_1,face_2,face_3,face_4,face_5)
    


    # define motors
    m_0 = Motor(3, 5, 7, 11)
    m_1 = Motor(13, 15, 19, 21)
    m_2 = Motor(23, 29, 31, 33)
    m_3 = Motor(8, 10, 12, 16)
    m_4 = Motor(18, 22, 24, 26)
    m_5 = Motor(32, 36, 38, 40)
    
    motors = [m_0, m_1, m_2, m_3, m_4, m_5]

    solution = Solver.solve(cube)
    print(solution)

    for inst in solution:
        print(inst)
        motors[inst[0]].quarter_turn(inst[1])


if __name__=='__main__':
    main()

