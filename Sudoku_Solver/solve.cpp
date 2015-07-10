#include<bits/stdc++.h>
#define ll long long int
#define rep(i,n) for(ll i=0;i<n;i++)
#define S second
#define F first
#define pb push_back
#define mp make_pair
#define all(v) v.begin(),v.end()
using namespace std;

int cb[9][9],a[9][9];
bool pv[9][9][10];
vector<pair<ll,pair<ll,ll> > > sz;
vector<pair<ll,pair<ll,ll> > > moves,rmval;

void init()
{
    rep(i,9)rep(j,9)rep(k,10)pv[i][j][k]=1;
    rep(i,9)rep(j,9)pv[i][j][0]=0;
    rep(i,9)rep(j,9)if(cb[i][j]!=0)rep(k,10)pv[i][j][k]=0;
    rep(i,rmval.size())pv[rmval[i].S.F][rmval[i].S.S][rmval[i].F]=0;
    rep(i,moves.size())pv[moves[i].S.F][moves[i].S.S][moves[i].F]=0;
}

void checkboard()
{
    int vis[9];
    rep(i,9)vis[i]=0;
    rep(i,9)
    {
        rep(j,9)vis[j]++;
        rep(j,9)if(vis[j]!=1)cout<<"Wrong at "<<i<<" "<<j<<endl;
        rep(i,9)vis[i]=0;
    }
    rep(i,9)vis[i]=0;
    rep(i,9)
    {
        rep(j,9)vis[j]++;
        rep(j,9)if(vis[j]!=1)cout<<"Wrong at "<<j<<" "<<i<<endl;
        rep(i,9)vis[i]=0;
    }
    cout<<"Correct!!"<<endl;
}

void eliminateregion(ll x, ll y)
{
    int xcheck[3],ycheck[3];
    if(x<3)
    {
        xcheck[0]=0;xcheck[1]=1;xcheck[2]=2;
    }
    else if(x>5)
    {
        xcheck[0]=6;xcheck[1]=7;xcheck[2]=8; 
    }
    else
    {
        xcheck[0]=3;xcheck[1]=4;xcheck[2]=5;
    }
    if(y<3)
    {
        ycheck[0]=0;ycheck[1]=1;ycheck[2]=2;
    }
    else if(y>5)
    {
        ycheck[0]=6;ycheck[1]=7;ycheck[2]=8; 
    }
    else
    {
        ycheck[0]=3;ycheck[1]=4;ycheck[2]=5;
    }
    rep(i,3)rep(j,3)pv[x][y][cb[xcheck[i]][ycheck[j]]]=0;    
}

void eliminateline(ll x,ll y)
{
    rep(i,9)pv[x][y][cb[x][i]]=0;
    rep(i,9)pv[x][y][cb[i][y]]=0;
}

void updatesz(ll x, ll y)
{
    ll cnt=0;
    for(ll i=1;i<10;i++)if(pv[x][y][i]==1)cnt++;
    sz.pb(mp(cnt,mp(x,y)));
}
void checkvalues()
{
    init();
    rep(i,9)rep(j,9)if(cb[i][j]==0){eliminateline(i,j);eliminateregion(i,j);}
    rep(i,9)rep(j,9)if(cb[i][j]==0)updatesz(i,j);
    sort(all(sz));
}
void makemove(ll x, ll y)
{
    rep(i,10)if(pv[x][y][i]==1){moves.pb(mp(i,mp(x,y)));cb[x][y]=i;return;}        
}
void managermval()
{
    rep(i,rmval.size())
    {
        ll flag=0;
        rep(j,moves.size())
        {
            if(rmval[i].S.F==moves[j].S.F&&rmval[i].S.S==moves[j].S.S)flag=1;   
        }
        if(flag==0){rmval.erase(rmval.begin()+i);i=-1;}
    }

}
void unmakemove()
{
    int val=moves[moves.size()-1].F;
    int x=moves[moves.size()-1].S.F;
    int y=moves[moves.size()-1].S.S;
    cb[x][y]=0;
    rmval.pb(mp(val,mp(x,y)));
    managermval();
    moves.pop_back();
}
ll cont=0;
void play()
{
    
    while(1)
    {   
        sz.clear();   
        checkvalues();
        if(sz.size()==0)break;
        if(sz[0].F==0)
            if(moves.size()>0)
                unmakemove();
            else
                {cout<<"ERROR"<<endl;break;}
        else           
            makemove(sz[0].S.F,sz[0].S.S);
        cont++;
    }   
}

int main()
{
    init();
    rep(i,9)rep(j,9){cin>>a[i][j];cb[i][j]=a[i][j];}
    play();
    cout<<"Finished in "<<cont<<" steps"<<endl;
    rep(i,9){rep(j,9)cout<<cb[i][j]<<" ";cout<<endl;}
    checkboard();
    return 0;
}
