import MeCab
import numpy as np
import re
import time

class TextAnalysis:
    
    def __init__(self,text_list) -> None:
        
        self.m = MeCab.Tagger("-Ochasen")
        #リスト
        self.text_list:list = text_list
        #文字列の長さ
        self.textlen_list:list = [len(i) for i in self.text_list]

        #文章を単語に分割
        self.textc_list:list = []
        for i in text_list:
          text = [line.split()[0] for line in self.m.parse(i).splitlines()]
          del text[-1]
          self.textc_list.append(text)
        
        #単語の長さ
        self.textclen_list:list = [[len(z) for z in i] for i in self.textc_list]

    def sentence_w(self,target_text:str) -> int:

        start = time.time()
        result_point:list = []
        point:int = 0
        #被っている文章を抽出します。
        target_text_list = [line.split()[0] for line in self.m.parse(target_text).splitlines()]
        del target_text_list[-1]
        
    
        if not not self.text_list:
            
            for textc in self.textc_list:
                #一致している単語を抽出
                w_text,text = [],[]
                for z in range(len(textc)):
                    for i in range(len(target_text_list)):
                        if target_text_list[i] == textc[z] and i not in w_text:
                            text.append([textc[z],z])
                            w_text.append(i)


                if not not w_text:
                    #連続している言葉を抽出
                    x = np.array(w_text)
                    result = []
                    tmp = [x[0]]
                    for i in range(len(x)-1):
                        if x[i+1] - x[i] == 1:
                            tmp.append(x[i+1])
                        else:
                            if len(tmp) > 0:
                                result.append(tmp)
                            tmp = []
                            tmp.append(x[i+1])
                    result.append(tmp)
                    result = [len(i) for i in result]

                    #驚異をポイント化
                    result_point_tmp:int = 0
                    for i in result:
                        result_point_tmp += i**2 

                    result_point.append(result_point_tmp)
                else:
                    result_point.append(0)
            #print(f"文字列処理時間:{time.time() - start}")

            #ポイント化

            print(sorted(result_point))
            q_all = np.percentile(result_point, [i*10 for i in range(len(self.text_list))])
            print(self.textlen_list)
            print(list(q_all))
            #if len(self.text_list) >= 5 and q25 >= 1:
            #    
            #    if 0 <= q25-q50 < 10:
            #        point += 60
            #    elif 0 <= q25-q50 < 20:
            #        point += 40
            #    
            #    if 0 <= q25-q75 < 10:
            #        point += 120
            #    elif 0 <= q25-q75 < 20:
            #        point += 60
       
        #return point



#"テスト","ではない","テスト","実験","まあー","適当"
#
    
if __name__ == "__main__":
    text_list = ["テスト","ではない","テスト","実験","まあー","適当"]

    textdata = TextAnalysis(text_list)

    point_list = textdata.sentence_w(target_text="これもてすとだあ",)

    #print(point_list)

        
