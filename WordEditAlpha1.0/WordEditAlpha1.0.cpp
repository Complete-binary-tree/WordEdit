#include<iostream>
#include<windows.h>
#include<vector>
#include<fstream>
#include<sstream>
#include<random>
#include<time.h>
#include<conio.h>
using namespace std;

#define wordeditversion "alpha1.0"
//#define DEBUG

mt19937 rd(time(0));

namespace tools{
    /// @brief �ù�궨λ��ָ��λ�á�
    /// @param x λ�õĺ�����
    /// @param y λ�õ�������
    void gotoxy(short x, short y) {
        COORD coord = {x, y}; 
        SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE),coord);
    }

    /// @brief ���ַ������ո���Ϊ��������ո���ַ�����
    /// @param s Ҫ��ֵ��ַ�����
    /// @return �ַ������飬���к������в����ո���ַ�����
    vector<string> dividestring(string s){
        vector<string>tmp;
        string lin;
        istringstream sin(s);
        while(sin>>lin){
            tmp.push_back(lin);
        }
        return tmp;
    }
};
using namespace tools;

struct IO{
    vector<string>wordEnglish;
    vector<vector<string>>wordChinese;
    vector<int>wordProficient;
    int n;
    bool Readed;
    int bowl[6];

    /// @brief ��ȡӢ�ﵥ���ļ���
    inline void read(){
        ifstream in("words.dat");
        in>>n;
#ifdef DEBUG
        cerr<<"debug:Reading the file \"words.dat\".\n";
#endif
        for(int i=0;i<n;++i){
            string tmp,tmp2;

            //��ȡ����
            getline(in,tmp);

            //��������
            getline(in,tmp);
            wordEnglish.push_back(tmp);

            //����Ӣ��
            getline(in,tmp);
            wordChinese.push_back(dividestring(tmp));
            
            //����������
            int a;
            in>>a;
            wordProficient.push_back(a);
            bowl[a]++;
        }
#ifdef DEBUG
    cerr<<"debug:Reading done!\n";
#endif
        Readed=1;
    }

    /// @brief �����Ӣ�ﵥ���ļ���
    inline void write(){
        if(Readed){
            //��ʽ
            //n
            //<English>
            //<Chinese1> <Chinese2> <Chinese3> ...
            ofstream out("words.dat");
            out<<n<<'\n';
            for(int i=0;i<n;++i){
                out<<wordEnglish[i]<<'\n';
                for(auto x:wordChinese[i])out<<x<<' ';
                out<<'\n';
                out<<wordProficient[i]<<'\n';
            }
            out.close();
        }
#ifdef DEBUG
        else{
            cerr<<"debug:didn't readed.\n";
        }
#endif
    }

    /// @brief ����Ӣ���Ƿ���ȷ��
    /// @param id �� wordEnglish �ı�š�
    /// @param answer ����Ĵ𰸡�
    /// @return ����Ƿ�ƥ�䡣
    ///
    /// ������Χʱ�ᴥ�� out of range ����
    inline bool checkEnglish(int id,string&answer){
        if(id>=wordEnglish.size()||id<0)  throw "IO::checkEnglish:out of range";
        return answer==wordEnglish[id];
    }

    /// @brief ���������Ƿ���ȷ��ֻҪ������һ����ȷ���ɡ�
    /// @param id �� wordChinese �ı�š�
    /// @param answer ����Ĵ𰸡�
    /// @return ����Ƿ�ƥ�䡣
    ///
    /// ������Χʱ�ᴥ�� out of range ����
    inline bool checkChinese(int id,vector<string> answer){
        if(id>=wordEnglish.size()||id<0)  throw "IO::checkEnglish:out of range";
        for(auto x:wordChinese[id])
            for(auto y:answer)
                if(x==y)
                    return 1;
        return 0;
    }

    /// @brief ��ʾӢ�ġ�
    /// @param id �� WordEnglish �ı�š�
    ///
    /// ������Χʱ�ᴥ�� out of range ����
    inline void showEnglish(int id){
        if(id>=wordEnglish.size()||id<0)  throw "IO::checkEnglish:out of range";
        cout<<wordEnglish[id];
    }

    /// @brief ��ʾ����
    /// @param id �� WordChinese �ı�š�
    ///
    /// ������Χʱ�ᴥ�� out of range ����
    inline void showChinese(int id){
        if(id>=wordEnglish.size()||id<0)  throw "IO::checkEnglish:out of range";
        for(auto x:wordChinese[id])
            cout<<x<<' ';
    }

    /// @brief �����ȡ���ʡ�
    /// @return ����id��
    inline int randomword(){
        int type=0;
        while(1){
            type=rd()%100;
            if(type<10)type=1;
            else if(type<40)type=2;
            else type=3;
            if(type==1&&bowl[1])break;
            if(type==2&&bowl[2])break;
            if(type==3&&(bowl[3]+bowl[4]+bowl[5]))break;
        }
        int id=0,i=0;
        if(type==1){
            type=rd()%bowl[1]+1;
            for(;id<n;++id){
                if(wordProficient[id]==1)++i;
                if(i==type)break;
            }
        }
        else if(type==2){
            type=rd()%bowl[2]+1;
            for(;id<n;++id){
                if(wordProficient[id]==2)++i;
                if(i==type)break;
            }
        }
        else{
            type=rd()%(bowl[3]+bowl[4]+bowl[5])+1;
            for(;id<n;++id){
                if(wordProficient[id]==3||wordProficient[id]==4||wordProficient[id]==5)++i;
                if(i==type)break;
            }
        }
        return id;
    }

    /// @brief ���в��ԣ��������ʣ���
    /// @return �Ƿ���ȷ���˳�����-1��
    inline int test(){
        cout<<"���뵥���� 0 ���˳���\n";
        int id=randomword();
        bool ret;
        if(rd()%2){
            system("cls");
            showChinese(id);
            cout<<"\n����������Ӣ�ġ�\n";
            string s;
            getline(cin,s);
            if(s=="0")return -1;
            if(checkEnglish(id,s)){
                cout<<"��ȷ��";
                bowl[wordProficient[id]]--;
                if(wordProficient[id]--==1)wordProficient[id]++;
                bowl[wordProficient[id]]++;
                ret=1;
            }
            else{
                cout<<"����ˣ�Ӧ���� ";
                showEnglish(id);
                cout<<"��";
                bowl[wordProficient[id]]--;
                wordProficient[id]=max(wordProficient[id]+2,5);
                bowl[wordProficient[id]]++;
                ret=0;
            }
            cout<<"\n�������������";
            while(_kbhit())_getch();
            _getch();
        }
        else{
            system("cls");
            showEnglish(id);
            cout<<"\n�������������ģ�����������Կո�ָ������� ';'��'��'��',' �ȷָ���ֻҪ������һ��������ȷ���ɣ�\n";
            string s;
            getline(cin,s);
            if(s=="0")return -1;
            if(checkChinese(id,dividestring(s))){
                cout<<"��ȷ��\n�𰸣�";
                showChinese(id);
                bowl[wordProficient[id]]--;
                if(wordProficient[id]--==1)wordProficient[id]++;
                bowl[wordProficient[id]]++;
                ret=1;
            }
            else{
                cout<<"����ˣ�Ӧ���ǣ�\n";
                showChinese(id);
                bowl[wordProficient[id]]--;
                wordProficient[id]=max(wordProficient[id]+2,5);
                bowl[wordProficient[id]]++;
                ret=0;
            }
            cout<<"\n�������������";
            while(_kbhit())_getch();
            _getch();
        }
        return ret;
    }

    /// @brief ��ӵ��ʡ�
    inline void addword(){
        system("cls");
        cout<<"1-�ֶ����\n2-�ļ����\n����-�˳�";
        while(_kbhit())_getch();
        char ch=_getch();
        system("cls");
        if(ch=='1'){
            cout<<"����һ��������0�˳���\n";
            while(1){
                string en,ch;
                cout<<"������Ӣ�ġ�\n";
                getline(cin,en);
                if(en==""||en=="0")break;
                cout<<"���������ġ�ÿ�����ļ��һ���ո�\n";
                getline(cin,ch);
                if(ch==""||en=="0")break;
                ++n;
                wordEnglish.push_back(en);
                wordChinese.push_back(dividestring(ch));
                wordProficient.push_back(5);
                bowl[5]++;
            }
        }
        else if(ch=='2'){
            cout<<"�ļ���ʽ-��һ��һ��������ʾ�������ĵ��ʸ�����\n������ÿ���������У�һ��Ӣ��һ�����ġ�\n��ͬ�����ÿո񣨶��� '��'��',' �ȷ��ţ�������\n�ļ���Ҫ��֤Ϊ GBK(ANSI) ���룬������ܳ������⡣\n";
            cout<<"�����ļ�����";
            string name;
            getline(cin,name);
            ifstream in(name);
            string s;
            int n;
            in>>n;
            this->n+=n;
            getline(cin,s);
            wordEnglish.push_back(s);
            wordChinese.push_back(dividestring(s));
            wordProficient.push_back(5);
            bowl[5]++;
        }
    }

    /// @brief ���к�����
    inline void testall(){
        system("cls");

        cout<<"WordEditAlpha v1.0\n";
        if(n==0){
            cout<<"�㻹û��ӵ���Ŷ��\n����������˳�\n";
            while(_kbhit())_getch();
            _getch();
            return;
        }
        cout<<"���е���\n";
        cout<<"����-1�����˳�";
        while(1){
            int ret=test();
            if(ret==-1)break;
        }
        write();
    }

    /// @brief ���캯����
    IO(){
        wordEnglish.clear();
        wordChinese.clear();
        wordProficient.clear();
        n=0;
        Readed=0;
        memset(bowl,0,sizeof bowl);
        //read();
    }
    ~IO(){
        write();
    }
};

struct Main{
    /// @brief չʾ�����档
    inline void showmain(){
        system("cls");
        cout<<"WordEditAlpha v1.0\n";
        cout<<"\n1-��ʼ����\n";
        cout<<"2-�ӵ���\n";
        cout<<"\n0-�˳�";
    }

    /// @brief ��������
    inline void main(){
#ifdef DEBUG
        cerr<<"debug:go into the main\n";
#endif
        cout<<"WordEditAlpha v1.0\n";
        cout<<"���ڼ��ص��ʡ���\n";
        IO a;
        a.read();
        showmain();
        while(1){
            while(_kbhit())_getch();
            char ch=_getch();
            if(ch=='1'){
                a.testall();
                showmain();
            }
            else if(ch=='2'){
                a.addword();
                showmain();
            }
            else if(ch=='0'){
                break;
            }
        }
    }
}M;

int main(){
    M.main();
    return 0;
}