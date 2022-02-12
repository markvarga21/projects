#include<iostream>
#include<exception>
#include<map>
#include<vector>

using namespace std;

enum Color {
	BLACK, WHITE
};

enum FigureName {
	DEFAULT, KIRALY, KIRALYNO, BASTYA, FUTO, LO, PARASZT
};

class Position {
private:
	int x, y;
public:
	Position()
	{
		x = y = -1;
	}
	Position(int xx, int yy) 
	{
		x = xx;
		y = yy;
	}
	int getPosX() { return x; }
	int getPosY() { return y; }

	void getPosXY() { cout << "(" << x << ", " << y << ")"; }

};

class ChessField {
public:
	int field[8][8];
	ChessField()
	{
		for (int i = 0; i < 8; ++i)
			for (int j = 0; j < 8; ++j)
				field[i][j] = 0;
	}

	void setStatus(Position pos, int status) 
	{ 
		int x = pos.getPosX(), y = pos.getPosY();
		field[x][y] = status; 
	}

	bool isOccupied (Position pos) 
	{ 
		int x = pos.getPosX(), y = pos.getPosY();
		if (field[x][y] == 1) return true;
		return false;
	}
};

bool isValidPos(Position pos)
{
	if (pos.getPosX() > 7 || pos.getPosX() < 0
		|| pos.getPosY() < 0 || pos.getPosY() > 7)
		return false;
	return true;
}

class Figure {
private:
	Position pos;
	FigureName name;
	vector<Position> possibleMoves;
public:
	Figure()
	{ 
		pos = Position(-1, -1);
		name = FigureName::DEFAULT;
	}

	Figure(Position xy, FigureName fn, ChessField& cf)
	{
		pos = xy;
		name = fn;
		cf.setStatus(pos, 1);

	}

	Position getFigPos() { return pos; }
	FigureName getFigName() { return name; }

	void getFigInfo() 
	{
		int x = pos.getPosX();
		int y = pos.getPosY();
		cout << "Figure position: " << x << " " << y << " and name enum index is: " << name  << endl;
	} 

	void setPossibleMoves(vector<Position> pos) { possibleMoves = pos; }

	vector<Position> getPossibleMoves() { return possibleMoves; }
};

void verticalSingleMoveCheck(Figure& f, ChessField cf, Color col)
{
	int x = f.getFigPos().getPosX(), y = f.getFigPos().getPosY();
	vector<Position> tempPos;

	switch(col) {
		// tegyuk fel, hogy a fekete fent van
		case Color::BLACK:
			// upward check
			if (isValidPos(Position(x+1, y)))
				if (!cf.isOccupied(Position(x+1, y)))
					tempPos.push_back(Position(x+1, y));
			break;
		// tegyuk fel, hogy a feher lent van
		case Color::WHITE:
			if (isValidPos(Position(x-1, y)))
				if (!cf.isOccupied(Position(x-1, y)))
					tempPos.push_back(Position(x-1, y));
			break;
		default:
			cerr << "Color not assigned!" << endl;
			break;
	}

	f.setPossibleMoves(tempPos);
}



int main()
{
	ChessField cf;
	Figure fig(Position(2, 2), FigureName::KIRALY, cf);
	/*
	if (cf.isOccupied(Position(1, 1)))
		cout << "This spot is occupied!" << endl;
	*/

	fig.getFigInfo();

	/*
	verticalSingleMoveCheck(fig, cf, Color::WHITE);

	vector<Position> moves = fig.getPossibleMoves();

	for (auto a : moves)
		a.getPosXY();
	*/
	return 0;
} 