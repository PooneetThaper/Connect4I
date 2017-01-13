#include <iostream>
#include <vector>
using namespace std;

double winAnalysis(vector<int> board,int move);
double contemplateMax(vector<int> board,int move);
double contemplateMin(vector<int> board,int move);


double winAnalysis(vector<int> board,int id){
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


double contemplateMax(vector<int> board, int move){
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

double contemplateMin(vector<int> board,int move){
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

int best_move(vector<int> a){
  double max=-1;
  int best=-1;
  for (size_t i = 0; i < 9; i++) {
    if(a[i]==0){
      double k=contemplateMin(a,i);
      cout<<i<<":"<<k<<"\n";
      if(k>max){
        max=k;
        best=i;
      }
    }
  }
  return best;
}

int main(){
  vector<int> a;
  a.push_back(-1);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  a.push_back(0);
  cout<<best_move(a)<<"\n";
}
