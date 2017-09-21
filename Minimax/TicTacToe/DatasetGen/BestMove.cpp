#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <utility>

using namespace std;

double winAnalysis(const vector<int>& board,const int& move);
double contemplateMax(vector<int> board,const int& move);
double contemplateMin(vector<int> board,const int& move);

double winAnalysis(const vector<int>& board,const int& id){
  double good=2;
  double bad=2;
  int count=0;
  int countBad=0;

  int n=0;
  //cout<<"good:"<<good<<"  bad:"<<bad<<"\n";
  //Horizontal Check
  for(n=0;n<9;n+=3){
    count=0;
    countBad=0;
    for(int i=n;i<n+3;i++){
      if(board[i]==id) count++;
      if(board[i]==(-id)) countBad++;
    }
    if(count==3) return 1;
    else{
      if(count==2 && countBad==0){
        bad=bad-1;
      }
      if(count==0 && countBad==2){
        good=good-1;
      }
    }
  }
  //cout<<"good:"<<good<<"  bad:"<<bad<<"\n";
  //Vertical Check
  for(n=0;n<3;n++){
    count=0;
    countBad=0;
    for(int i=n;i<9;i=i+3){
      if(board[i]==id) count++;
      if(board[i]==(-id)) countBad++;
    }
    if(count==3) return 1;
    else{
      if(count==2 && countBad==0){
        bad=bad-1;
      }
      if(count==0 && countBad==2){
        good=good-1;
      }
    }
  }
  //cout<<"good:"<<good<<"  bad:"<<bad<<"\n";
  //Diagonal Check from corner (move%3==move%6)
  //0 4 8
  //2 4 6
  n=0;
  if(board[n]==id){
    if(board[4]==id && board[8-n]==id) return 1;
    if(board[4]==id || board[8-n]==id){
      if(board[4]==0 || board[8-n]==0){
        bad=bad-1;
      }
    }
  }else{
    if(board[n]==-id){
      if(board[4]==-id || board[8-n]==-id){
        if(board[4]==0 || board[8-n]==0){
          good=good-1;
        }
      }
    }else{
      if(board[4]==id && board[8-n]==id) bad=bad-1;
      if(board[4]==id && board[8-n]==id) bad=bad-1;
    }
  }

  n=2;
  if(board[n]==id){
    if(board[4]==id && board[8-n]==id) return 1;
    if(board[4]==id || board[8-n]==id){
      if(board[4]==0 || board[8-n]==0){
        bad=bad-1;
      }
    }
  }else{
    if(board[n]==-id){
      if(board[4]==-id || board[8-n]==-id){
        if(board[4]==0 || board[8-n]==0){
          good=good-1;
        }
      }
    }else{
      if(board[4]==id && board[8-n]==id) bad=bad-1;
      if(board[4]==id && board[8-n]==id) bad=bad-1;
    }
  }

  //cout<<"good:"<<good<<"  bad:"<<bad<<"\n";
  //Diagonal Check from center

  /*
  if(board[4]==id){
    if(board[0]==id && board[8]==id) return 1;
    if(board[2]==id && board[6]==id) return 1;
    if(board[0]==id || board[8]==id) bad=bad-1;
    if(board[2]==id || board[6]==id) bad=bad-1;
  }else{
    if(board[0]==board[8]){
      if(board[0]==id) bad=bad-1;
      if(board[0]==-id) good=good-1;
    }
    if(board[2]==board[6]){
      if(board[2]==id) bad=bad-1;
      if(board[2]==-id) good=good-1;
    }
  }
  */
  //cout<<"good:"<<good<<"  bad:"<<bad<<"\n";
  return (good-bad)/2;
}


double contemplateMax(vector<int> board, const int& move){
  if(board[move]!=0) return -2;
  board[move]=-1;
  double winstat=winAnalysis(board,-1);
  /*
  for (size_t i = 0; i < 9; i++) {
      cout << board[i] << "\t";
  }
  cout <<":"<< winstat << '\n';
  */
  if(winstat==1) return winstat*-1;

  int best=-1;
  double max=-1;
  double sum=0;
  int count=0;
  for (size_t i = 0; i < 9; i++) {
    if (board[i]==0) {
      count++;
      double k=contemplateMin(board,i);
      sum+=k;
      if(k>=max){
        max=k;
        best=i;
      }
    }
  }
  if(count!=0){
    for(int i=0;i<9;i++){
      //cout<<board[i]<<",\t";
    }
    //cout<<best<<",max:"<<max<<"\n";
    return ((3*sum/count)-winstat)/4;
  }else return winstat*-1;
}

double contemplateMin(vector<int> board,const int& move){
  if(board[move]!=0) return -2;
  board[move]=1;
  double winstat=winAnalysis(board,1);
  /*
  for (size_t i = 0; i < 9; i++) {
      cout << board[i] << "\t";
  }
  cout <<":"<< winstat << '\n';
  */
  if(winstat==1) return winstat;

  int best=-1;
  double min=1;
  double sum=0;
  int count=0;
  for (size_t i = 0; i < 9; i++) {
    if (board[i]==0) {
      count++;
      double k=contemplateMax(board,i);
      sum+=k;
      if(k<=min){
        min=k;
        best=i;
      }
    }
  }
  if(count!=0){
    for(int i=0;i<9;i++){
      //cout<<board[i]<<",\t";
    }
    //cout<<best<<",min:"<<min<<"\n";
    return ((3*sum/count)+winstat)/4;
  }else return winstat;
}

int best_move(const vector<int>& a, bool show=false){
  double max=-1;
  int best=-1;
  for (size_t i = 0; i < 9; i++) {
    if(a[i]==0){
      double k=contemplateMin(a,i);
      if (show) cout<<i<<":"<<k<<"\n";
      if(k>max){
        max=k;
        best=i;
      }
    }
  }
  if (show) cout<< best << "\n\n";
  return best;
}

void printBoard(const vector<int>& board){
  for(int i=0;i<3;i++){
    for(int j=0;j<3;j++){
      cout<< board[i*3 + j] << "\t";
    }
    cout<<"\n\n";
  }
}

vector<int> reverseBoard(vector<int> board){
  for(int i=0;i<9;i++){
    board[i]=board[i]*-1;
  }
  return board;
}

void makeMove(vector<int>& board, int playerNum, int move){
  board[move]=playerNum;
}

//copied from try 3 to find completion
bool over(const vector<int>& board){
  //Return value returns bool for whether or not this is an end state and a score
  //Diagonal win check
  if ((board[0]==board[8] && board[0]==board[4]) || (board[2]==board[6] && board[2]==board[4])){
    if (board[4]==1) return true;
    if (board[4]==-1) return true;
  }
  //Horizontal win check
  for(int n=0;n<9;n=n+3){
    if (board[n]==board[n+1] && board[n+1]==board[n+2]){
      if (board[n]==1) return true;
      if (board[n]==-1) return true;
    }
  }
  //Vertical win check
  for(int n=0;n<3;n=n+1){
    if (board[n]==board[n+3] && board[n+3]==board[n+6]){
      if (board[n]==1) return true;
      if (board[n]==-1) return true;
    }
  }
  //No win found (can either be a draw or a nonterminal state)
  for(int i=0;i<9;i++){
    if (board[i]==0) return false;
    //Game still playable
  }
  //Draw (all other cases exhausted)
  return true;
}

void demo(vector<int> a,bool againstUser){
  printBoard(a);
  for(int player=-1;!over(a);player=player*-1){
    if (player==1) {
      makeMove(a,1,best_move(a,true));
    }else{
      if(!againstUser){
        makeMove(a,-1,best_move(reverseBoard(a),true));
      }else{
        cout<< "Pick your move (0-8):\n";
        int move;
        cin >> move;
        if(a[move]==0) makeMove(a,-1,move);
      }

    }
    printBoard(a);
  }
}

vector<int> decodeBase3(int coded){
  vector<int> retval;
  for (int i = 0; i < 9; i++) {
    retval.push_back(0);
  }
  for (int i = 8; i >=0; i--) {
    int next = coded/3;
    retval[i]= coded - (next*3) -1;
    coded = next;
  }
  return retval;
}

int main(){
  //Change these booleans for demos
  //demoTime runs demo
  bool demoTime = true;
  //userInput decides whether demos is cpu v cpu or user v cpu
  bool userInput = false;
  vector<int> a;
  //written out for debugging to plug in starting state
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  if(demoTime){
    demo(a,userInput);
  }else{
    vector<pair<int,int> > codedBoards;
    string line;
    ifstream boardList ("OutputFiles/nonterminalBoards.txt");
    if (boardList.is_open()){
      while(getline(boardList,line)){
         codedBoards.push_back(pair<int,int>(stoi(line),0));
      }
      boardList.close();
    }

    int num=codedBoards.size();
    cout << "Successfully read " << num << " coded boards\n";

    for (int i = 0; i < num; i++) {
      if (i%100==1) cout << i << "\n";
      codedBoards[i].second = best_move(decodeBase3(codedBoards[i].first));
    }

    ofstream labeledOutput ("OutputFiles/bestMoves.txt");
    if (labeledOutput.is_open()){
      for (int i = 0; i < num; i++) {
        labeledOutput << codedBoards[i].first << ":" << codedBoards[i].second << "\n";
      }
      labeledOutput.close();
    }
  }
  return 0;
}
