if __name__=="__main__":
    print("Libaries Loading")
import matplotlib.pyplot as plt
from mpmath import harmonic, mp, exp, loggamma,log,polygamma,sqrt,re,cbrt
from math import log10,floor,ceil
import numbers
from scipy.special._ufuncs import _beta_ppf
mp.dps=25
if __name__=="__main__":
    print("Libaries Loaded")
class Beta():
    def __init__(self,a,b):
        self.a=(a)
        self.b=(b)
        self.n=a+b
        self.logNormalazationConstant=loggamma(a+b+2)-loggamma(a+1)-loggamma(b+1)
        self.mode,self.mean,self.variance,self.stdev,self.invstdev=None,None,None,None,None
        self._stats_computed=False
    def computeStats(self):
        if not self._stats_computed:
            if self.n==0:
                self.mode=None
            else:
                self.mode=self.a/self.n
            self.mean=(self.a+1)/(self.n+2)
            self.variance=((self.a+1)*(self.b+1))/((self.n+2)*(self.n+2)*(self.n+3))
            self.stdev=(sqrt(self.variance))
            self.invstdev=(sqrt((self.n+2)*(self.n+2)*(self.n+3)/((self.a+1)*(self.b+1))))
            self._stats_computed=True
    def pdf(self,x):
        if x==1:
            if self.b==0:
                return (1+self.a)
            return 0
        elif x==0:
            if self.a==0:
                return (1+self.b)
            return 0
        lnx=log(x)
        lnxc=log(1-x)
        return (exp(self.logNormalazationConstant+self.a*lnx+self.b*lnxc))  
def highestProbDistBeliefForBetaDist(a,b):
    t=exp(harmonic(a)-harmonic(b))
    return (1-1/(1+t))
def dydxForOptimalBeta(a,n):
    "computes dy/dx for the plot of the optimal max beta beliefs very complicated formula"
    b=n-a
    lnx=harmonic(a)-harmonic(b)
    xplus=1+exp(lnx)
    return (exp(loggamma(n+2)-loggamma(a+1)-loggamma(b+1)+(a-1)*lnx-log(xplus)*(n-2))*(a-n+n/xplus))
def dydaForOptimalBetaYandX(a,n):
    "computes dy/da for the plot of the optimal max beta beliefs very complicated formula"
    b=n-a
    lnx=harmonic(a)-harmonic(b)
    xplus=1+exp(lnx)
    y=(exp(loggamma(n+2)-loggamma(a+1)-loggamma(b+1)+a*lnx-n*log(xplus)))   
    return (y*(a-n+n/xplus)*(polygamma(1,a+1)-polygamma(1,b+1))),(y),(1-1/(1+exp(lnx)))
def dadxForOptimalBetaYandX(a,n):
    b=n-a
    lnx=harmonic(a)-harmonic(b)
    xplus=1+exp(lnx)
    y=(exp(loggamma(n+2)-loggamma(a+1)-loggamma(b+1)+a*lnx-n*log(xplus))) 
def ddydxdxAndOtherInfo(a,n):
    """Computes ddy/dxdx for the plot of optimal max bet beliefs among other things very long formulas
    returns ddy/dxdx,da/dx,y,x"""
    b=n-a
    ΔH=harmonic(a)-harmonic(b)
    expΔH=exp(ΔH)
    expΔHplus1=1+expΔH
    x=1-1/expΔHplus1
    di,tri=polygamma(1,a+1)+polygamma(1,b+1),polygamma(2,a+1)-polygamma(2,b+1)    
    dlnyda=(a-n*x)*di
    dadx=expΔHplus1/(x*di)
    ddlnydada=di+(a-n*x)*tri-n*x*di*di/expΔHplus1
    lny=loggamma(n+2)-loggamma(a+1)-loggamma(b+1)+a*log(x)+b*log(1-x)
    dxdxdada=x*((1-2*x)*di*di+tri)/expΔHplus1
    lnddydxdx=lny+2*log(dadx)+log(ddlnydada+dlnyda*(dlnyda-dadx*dxdxdada))
    return (re(exp(lnddydxdx))),(dadx),(exp(lny)),(x)
def maxProb(a,n):
    b=n-a
    lnx=harmonic(a)-harmonic(b)
    xplus=1+exp(lnx)
    return (exp(loggamma(n+2)-loggamma(a+1)-loggamma(b+1)+a*lnx-n*log(xplus)))
def derivatives(y:numbers.Real,x:numbers.Real,a:numbers.Real,b:numbers.Real,multi:numbers.Real=1,divi:numbers.Real=1):
    "returns dydx,ddydxdx for beta distrubtion ∝x^a(1-x)^b with prob density y at point x"
    match x:
        case 0:
            dydx=-b*y
            ddydxdx=b*(b-1)*y
            #dddydxdxdx=b*(b*(3-b)-2)*y
        case 1:
            dydx=a*y
            ddydxdx=a*(a-1)*y
            #dddydxdxdx=a*(a*(a-3)+2)*y
        case _:
            xc=1-x
            tmp1=a/x-b/xc
            dydx=y*tmp1
            xsq,xsqc=x*x,xc*xc
            #xcb,xcbc=xsq*x,xsqc*x
            tmp2=a/xsq+b/xsqc
            #tmp3=a/xcb-b/xcbc
            ddydxdx=y*(tmp1*tmp1-tmp2)
            #dddydxdxdx=y*(tmp1**3-3*tmp1*tmp2+2*tmp3)
    return multi*dydx/divi,multi*ddydxdx/divi#,multi*dddydxdxdx/divi
class dda:
    def __init__(self,successes,failures,d,maxY,stdev:None):
        self.successes=successes
        self.failures=failures
        self.d=d
        self.maxY=maxY
        self._dadx=1
        self.X=[]
    def f(self,a):
        self.slope,self._dadx,y,x=ddydxdxAndOtherInfo(a+self.successes,self.d+self.successes+self.failures)
        self.X.append(x)
        return y
    def dadx(self,x):
        return self._dadx
    def ddydxdx(self,x,y):
        return self.slope      
class RobustBayesianAnalysis():
    MAXBINOMINALN=2<<31
    MAXPROB=2<<30
    MAX64INT=2<<63-1
    def __init__(self,d,an:int=150,successes:int=0,failures:int=0):
        """"   
           d : Degree of Prior Certitude of Beliefs
           an : Asymptotic number of points calculated (can be as low as 75 and still give good results)
           successes : Observed successes defaults to 0
           failures  : Observed failures defaults to 0
        """
        self.d=d
        self.an=an
        self.h=6.61889/(an**3)
        self.HPDB=highestProbDistBeliefForBetaDist
        self.successes=successes
        self.failures=failures
        self.sqrt2=sqrt(2)
        self.cbrt6=cbrt(6)
        self.multi=1
    def maxVar(self):
        a,b=self.successes,self.failures
        if self.successes>self.failures:
            a,b=b,a
        aoptimal=float(((.75*b+7/6)**2-1/9)**.5-(.25*b+1.5))#in case of mpmath
        if aoptimal>a:
            a=min(a+self.d,aoptimal)
        beta=Beta(a,b)
        beta.computeStats()
        return beta.variance
    def maxStdev(self):
        return self.maxVar()**.5
    def sampler(self,f,ddfdxdx,h,upperbound,lowerbound,multi:numbers.Real=1,x=None,minimum=0,dadx=lambda x:1):
        "f is functions with one parameter x"
        "ddydxdx is a function with 2 parameters x,y"
        "Returns X,Y"
        if x==None:
            x=lowerbound        
        X,Y=[],[]      
        while lowerbound<=x and x<=upperbound:
            y=f(x)
            if y<=minimum:
                return X,Y
            Y.append(y)
            X.append(x)
            ddydxdx=abs(ddfdxdx(x,y))
            if ddydxdx==0:
                return X,Y        
            x+=multi*self.cbrt6*cbrt(h/ddydxdx)*dadx(x)           
        return X,Y
    def computeGraph(self,ends:bool=None):
        """
        ends: If False cuts outs the regions with less than .1% relative likelyhood from the graph recommened when dealing with 10**6 or more datapoints
        """        
        if ends==None:
            ends=(self.successes+self.failures+self.d)<(2<<16)
        self.lowerBeta,self.upperBeta=Beta(self.successes,self.d+self.failures),Beta(self.d+self.successes,self.failures)
        self.upperBeta.computeStats()
        self.lowerBeta.computeStats()
        self.maxstdev=self.maxStdev()
        a,b=self.successes,self.failures
        if self.successes<self.failures:
            a,b=b,a
        self.minvarBeta=Beta(a+self.d,b)
        self.minvarBeta.computeStats()
        mp.dps=max(25,7+int(-1*log(self.minvarBeta.stdev/self.an)))        
        lowerBound,upperBound=self.HPDB(self.lowerBeta.a,self.lowerBeta.b),self.HPDB(self.upperBeta.a,self.upperBeta.b)
        swappoint=1/(1+exp(sum([log(self.failures+1+k)-log(self.successes+1+k) for k in range(self.d)])/self.d))
        X,upperProb,XLow,maxY=[],[],[],1
        if ends:
            X.append(0)
            upperProb.append(self.lowerBeta.pdf(0))
        if self.successes>self.failures:
            maxY=self.upperBeta.pdf(self.upperBeta.mode)
        else:
            maxY=self.lowerBeta.pdf(self.lowerBeta.mode)
        minimum=0
        if not ends:
            minimum=maxY/1000
        ddydxdx=lambda x,y:derivatives(y,x,self.successes,self.d+self.failures,1,1)[1] #maxY*self.lowerBeta.stdev
        Xt,Yt=self.sampler(self.lowerBeta.pdf,ddydxdx,self.h,lowerBound,0,-1,lowerBound,minimum)
        X.extend(reversed(Xt))
        upperProb.extend(reversed(Yt))
        lowerProb=[self.upperBeta.pdf(x) for x in X]
        XLow.extend(X)
        asamp=dda(self.successes,self.failures,self.d,maxY,self.maxstdev)
        Yt=self.sampler(asamp.f,asamp.ddydxdx,self.h,self.d,0,dadx=asamp.dadx)[1]
        X.extend(asamp.X)
        upperProb.extend(Yt)                 
        ddydxdx=lambda x,y:derivatives(y,x,self.successes+self.d,self.failures,1,1)[1] #maxY*self.upperBeta.stdev)
        Xt,Yt=self.sampler(self.upperBeta.pdf,ddydxdx,self.h,swappoint,lowerBound,-1,swappoint)
        XLow.extend(reversed(Xt))
        lowerProb.extend(reversed(Yt))                     
        ddydxdx=lambda x,y:derivatives(y,x,self.successes,self.d+self.failures,1,1)[1] #maxY*self.lowerBeta.stdev
        Xt,Yt=self.sampler(self.lowerBeta.pdf,ddydxdx,self.h,upperBound,swappoint,1,swappoint)
        XLow.extend(Xt)
        lowerProb.extend(Yt)
        ddydxdx=lambda x,y:derivatives(y,x,self.successes+self.d,self.failures,1,1)[1] #maxY*self.upperBeta.stdev
        Xt,Yt=self.sampler(self.upperBeta.pdf,ddydxdx,self.h,1,upperBound,1,upperBound,minimum)
        if ends:
            Xt.append(1)
            Yt.append(self.upperBeta.pdf(1))
        X.extend(Xt)
        upperProb.extend(Yt)
        lowerProb.extend([self.lowerBeta.pdf(x) for x in Xt])
        XLow.extend(Xt)
        if maxY>self.MAXPROB:
            upperProb=[y/maxY for y in upperProb]
            lowerProb=[y/maxY for y in lowerProb]
            print("MaxY="+str(maxY))         
        return X,upperProb,XLow,lowerProb        
    def plotBeta(self,a,b,ends:bool=None):
        print("------------------------------------")
        print("a:{a}\tb:{b}".format(a=a,b=b))
        if ends==None:
            ends=(self.successes+self.failures+self.d)<(2<<16)        
        beta=Beta(a,b)
        beta.computeStats()
        print("Mean:{0:3g}".format(float(beta.mean)))        
        print("Mode:{0:3g}".format(float(beta.mode)))
        print("Beta Standard Deviation:{0:3g}".format(float(beta.stdev)))
        self.reasonablevaluesprint([_beta_ppf(.05,a+1,b+1),_beta_ppf(.95,a+1,b+1)],"",3,"[]","Reasonable 90% Equal-Tailed Credible Interval is")
        mp.dps=max(25,7+int(-1*log(beta.stdev/self.an)))
        maxY=beta.pdf(beta.mode)
        minimum=0
        if not ends:
            minimum=maxY/1000
        X,Prob=[],[]
        if ends:
            X.append(0)
            Prob.append(beta.pdf(0))
        ddydxdx=lambda x,y:derivatives(y,x,a,b)[1]
        Xt,Yt=self.sampler(beta.pdf,ddydxdx,self.h,beta.mode,0,-1,beta.mode,minimum)   
        X.extend(reversed(Xt))
        Prob.extend(reversed(Yt))
        Xt,Yt=self.sampler(beta.pdf,ddydxdx,self.h,1,beta.mode,1,beta.mode,minimum)
        X.extend(Xt)
        Prob.extend(Yt)
        if ends:
            X.append(1)
            Prob.append(beta.pdf(1)) 
        plt.plot(X,Prob)
        plt.xlabel("Population Success Probabilty")
        plt.ylabel("Probabilty")  
        plt.title("B(x;{0},{1})".format(a,b))
        plt.show()            
    def reasonablevaluesprint(self,region,parameter_name:str="",sig_digits:int=3,format:str="pm",override:str=None):
        """
        region is a list or tuple in the following format [low1,upp1,low2,upp2,...,low_n,upp_n] which contains the reasonable values.
        parameter_name is the name of the parameter if not specifed is ommitted.
        sig_digits is the amount of digits after lower and upper disagree that is displayed.
        format is a string and can be "pm" "[]" or "wordy".
        "pm" reasonable values printed as x±y
        "[]" reasonable values printed as [low,upp]
        "wordy" reasonable values printed as "{low} to {upp}"
        """
        region=[float(r) for r in region]
        if format not in {"pm","[]","wordy"}:
            format="pm"
        if override==None:
            print("Reasonable Beliefs about the {0} are".format(parameter_name.capitalize()),end="")
        else:
            print(override,end="")
        output=""
        for low,upp in zip(region[::2],region[1::2]):
            if low==upp:
                output+=" the value{0:#.{s}g}".format(low,s=sig_digits)
            else:
                diff=abs(low-upp)
                agree_order=floor(log10(diff))
                if format=="pm":
                    middle=(low+upp)/2
                    middle,diff=round(middle,sig_digits-agree_order),round(diff,sig_digits-agree_order)
                    output+=" {0:g} ± {1:g} and".format(middle,diff,n=sig_digits-agree_order)
                else:
                    low,upp=min(low,upp,key=lambda x:abs(x)),max(upp,low,key=lambda x:abs(x))
                    if low==0:
                        agree_order=min(agree_order,ceil(log10(abs(upp))))
                    else:
                        agree_order=min(agree_order,ceil(log10(abs(low))))
                    low,upp=round(low,sig_digits-agree_order),round(upp,sig_digits-agree_order)                    
                    if format== "[]":
                        output+=" [{0:g},{1:g}] and".format(low,upp)
                    elif format== "wordy":
                        output+=" from {0:g} to {1:g} and".format(low,upp)
        print(output[:-4])
    def stats(self,ends:bool=None,posteior:bool=True,MoreAnalysis=None):
        """
        ends: If False cuts outs the regions with less than .1% relative likelyhood from the graph recommened when dealing with 10**6 or more datapoints
        posteior: If False displays and gives statistics as prior not posteior
        MoreAnalysis function that does stuff with the data right before it plots for doing more analysis to the data
        """
        print("------------------------------------")
        print("Successes:{0}\tFailures:{1}\tTotal:{2}".format(self.successes,self.failures,self.successes+self.failures))
        X,upperProb,XLow,lowerProb=self.computeGraph(ends)
        a,b=self.successes,self.failures
        if self.successes<self.failures:
            a,b=b,a
        minvarBeta=Beta(a+self.d,b)
        minvarBeta.computeStats()
        self.reasonablevaluesprint((self.lowerBeta.mean,self.upperBeta.mean),"mean") 
        self.reasonablevaluesprint((self.lowerBeta.mode,self.upperBeta.mode),"mode") 
        self.reasonablevaluesprint((minvarBeta.stdev,self.maxstdev),"standard deviation of Beta dist")
        at,bt=self.successes+1,self.failures+1
        if at+self.d>RobustBayesianAnalysis.MAX64INT:
            at=float(at)
        if bt+self.d>RobustBayesianAnalysis.MAX64INT:
            bt=float(bt)
        self.reasonablevaluesprint([_beta_ppf(.05,at,bt+self.d),_beta_ppf(.95,at+self.d,bt)],"",3,"[]","Reasonable 90% Equal-Tailed Credible Interval is")
        self.reasonablevaluesprint([_beta_ppf(.025,at,bt+self.d),_beta_ppf(.975,at+self.d,bt)],"",3,"[]","Reasonable 95% Equal-Tailed Credible Interval is")
        self.reasonablevaluesprint([_beta_ppf(.005,at,bt+self.d),_beta_ppf(.995,at+self.d,bt)],"",3,"[]","Reasonable 99% Equal-Tailed Credible Interval is")
        if MoreAnalysis!=None:
            return MoreAnalysis(vars())
        plt.plot(X,upperProb)#,"k")
        plt.plot(XLow,lowerProb)#,"k",linestyle="--")
        plt.xlabel("Population Success Probabilty")
        plt.ylabel("Probabilty")
        plt.title("Reasonable Postetiors")
        plt.legend(["Upper Probabilty","Lower Probabilty"])
        plt.show()   
class rand:
    _called=False
    binomial=None
    normal=None
    def __init__(self):
        if not rand._called:
            import numpy.random as random
            rng=random.Generator(random.SFC64())
            rand.binomial=lambda n,p:rng.binomial(n,p)
            rand.normal=lambda mu,stdev:rng.normal(mu,stdev)
class Demo(RobustBayesianAnalysis):
    def __init__(self,p,n,an):
        """p : Population Success Probabilty
           n : Degree of Prior Certitude of Beliefs
           an : Asymptotic number of points calculated (can be as low as 50 and still give good results)
        """              
        super().__init__(n,an)
        self.p=p
        rand()
    def getData(self,n):
        "perform n samples of the population"
        if n<self.MAXBINOMINALN:
            successes=rand.binomial(n,self.p)
        else:
            stdev=(sqrt(n*self.p*(1-self.p)))
            successes=round(rand.normal(self.p*n,stdev))
        failures=n-successes
        self.successes+=successes
        self.failures+=failures
        print("------------------------------------")        
        print("Observed {0} Successes and {1} Failures".format(successes,failures))
        print("Total Successes {0} out of {1}".format(self.successes,self.successes+self.failures))        
if __name__=="__main__":      
    s,f,t,x,y,h=2,10,10,0,0,.01
    var=lambda a,b:(a+1)*(b+1)/((a+b+3)*(a+b+2)**2)
    maxVar,cords=0,[]
    while x<=t:
        y,yt=0,t-x
        while y<=yt:
            v=var(s+x,f+y)
            if v>maxVar:
                maxVar=v
                cords=[s+x,f+y]
            y+=h
        x+=h
    print(maxVar,cords)
    tmp=RobustBayesianAnalysis(t,150,s,f)
    input(tmp.maxVar())
    Analysis=Demo(.7,10,250)  
    Analysis.stats(True,False)
    while True:
        Analysis.getData(10)
        Analysis.stats()