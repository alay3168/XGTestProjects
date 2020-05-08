# coding=utf-8
import numpy as np
import matplotlib as mpl

mpl.use('Agg')
from scipy import interp, sparse
import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import roc_curve, auc, precision_recall_curve
import time
from sklearn.metrics.pairwise import cosine_similarity
from PIL import ImageFont, Image, ImageDraw
import sys, os, datetime, random, math
from sklearn.preprocessing import normalize


matplotlib.use('Agg')
DrawWrong = False
DrawWrongThreshold = 0.8
PlotMerge = False
PrintTop1Pairs = False
minStartThreshold = 0
test = False


def todict(array, kind, dest=[]):
    if kind == 1:
        return dict(zip(array, [1] * len(array)))
    elif kind == 0:
        return dict(zip(array, range(len(array))))
    else:
        return dict(zip(array, dest))


def tonddic(array):
    ret = [999999] * len(array)
    for i in range(len(array)):
        ret[array[i]] = i
    return np.array(ret)


def checkexists(v, dic):
    return dic.has_key(v)


def getlabels(file):
    global GroundTruth
    lines = open(file).read().replace("\n", " ").split(" ")[:-1]
    size = len(lines)
    labels = np.array(lines).reshape((-1, 3))
    gallery = np.where(labels[:, 2] == "0")[0]
    query = np.where(labels[:, 2] == "1")[0]
    dic = todict(labels[gallery][:, 1], 1)
    vfunc = np.vectorize(checkexists)
    GroundTruth = vfunc(labels[query][:, 1], dic)
    print GroundTruth
    print ('GroundTruth.sum:', GroundTruth.sum())
    print "gallery", len(gallery), "query", len(query)
    # print(list(labels[query][~GroundTruth]))
    return labels, gallery, query


def readFeatures(filename, size, dtype="cos"):
    flines = open(filename).read()
    fs = map(float, flines.replace("\n", " ").split(" ")[:-1])
    feats = np.array(fs, dtype='f')
    t = feats.shape[0]
    feat_dim = int(1.0 * feats.shape[0] / size)
    print "Feature dim: %d" % feat_dim
    feats = feats[:size * feat_dim, ...].reshape((size, -1))
    # print "distance type =",dtype
    if test:
        return feats
    feats = normalize(feats) if dtype == "cos" else feats
    # print(feats.shape)
    return feats


def paste(img, pic, pos):
    if len(pic) == 0:
        return img
    try:
        img1 = Image.open(pic)
        img.paste(img1, pos)
    except:
        print "can not find img", pic
        return img
    return img


def merge(pic1, pic2, pic3, info1, info2, output):
    merge_img = Image.new('RGB', (1200, 420), 0xffffff)
    merge_img = paste(merge_img, pic1, (0, 20))
    merge_img = paste(merge_img, pic2, (400, 20))
    merge_img = paste(merge_img, pic3, (800, 20))
    # pic4=[pic3[0].replace("sr","xinjiang")]
    # print pic1,pic2,pic3
    # merge_img = paste(merge_img,pic4,(1200,20))
    draw = ImageDraw.Draw(merge_img)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', 18)
    draw.text((0, 0), "query", fill="red", font=font)
    draw.text((400, 0), "groundtruth: " + str(round(info1, 3)), fill="red", font=font)
    draw.text((800, 0), "predict : " + str(round(info2, 3)), fill="red", font=font)
    merge_img.save(output, quality=100)


def score(dist):
    s = (1 + dist) / 2
    return s


def drawTop1(labels, query, gallery, y_true, y_score, features, top1, filename=""):
    querys = labels[query]
    gallerys = labels[gallery]
    gdic = todict(gallerys[:, 1], 0)
    #    gnddic=tonddict(gallerys[:,1])
    print "printing pairs!"
    if PrintTop1Pairs:
        out = open("Top1Pairs", "w")
        i = 0
        for label in querys:
            lb = label[1]
            if gdic.has_key(lb):
                fn = gallerys[gdic[lb]][0]
                gscore = (2 - np.sum((features[query[i]] - features[gallery[gdic[lb]]]) ** 2)) / 2
            else:
                fn = ""
                gscore = 0.0
            print >> out, label[0], fn, gallerys[top1[i]][0], gscore, y_score[i]
            i += 1
        out.close()

    if DrawWrong:
        print "Drawing wrong"
        if len(features) == 0:
            features = readFeatures(filename, len(labels))
        cnt = 0
        out = open("drawwrong", "w")
        print y_true.shape, y_score.shape
        pos = np.where((y_true == False) & (y_score > DrawWrongThreshold))[0]
        # pos=np.where( (y_true==True) & (y_score<DrawWrongThreshold) )[0]
        print "number:", len(pos)

        for i in pos:
            name1 = querys[i][0]
            lb = querys[i][1]
            if gdic.has_key(lb):
                name2 = gallerys[gdic[lb]][0]
                gscore = (2 - np.sum((features[query[i]] - features[gallery[gdic[lb]]]) ** 2)) / 2
            else:
                name2 = ""
                gscore = 0.0
            name3 = gallerys[top1[i]][0]
            merge(name1, name2, name3, gscore, y_score[i], str(cnt) + ".jpg")
            print >> out, cnt, name1, name2, name3, gscore, y_score[i]
            cnt += 1
        out.close()
        print "done drawing!"


def saveData(true, score, filename, mat, index, shape):
    np.savez(filename, mat=mat, index=index, true=true, score=score, shape=shape)


def loadData(filename):
    try:
        npzfiles = np.load(filename)
        mat = npzfiles["mat"]
        index = npzfiles["index"]
        y_true = npzfiles["true"]
        y_score = npzfiles["score"]
        shape = npzfiles["shape"]
        return y_true, y_score, mat, index, shape
    except:
        print "Need to update npz file for newer version"
        sys.exit()


def getScores(filename, labels, gallery, query, kind):
    global GroundTruth, Predict_True
    # print "gallery",len(gallery),"query",len(query)
    # print(labels)
    rocfile = filename + ".npz"
    if os.path.exists(filename + ".npz"):
        y_true, y_score, mat, index, shape = loadData(rocfile)
        print(y_score)

        import shutil
        querys = labels[query]
        gallerys = labels[gallery]

        # index = np.argpartition(mat, -1)
        index_max = index[:, -1]
        ind = np.arange(index.shape[0])[:, None]
        top1 = index_max.reshape(-1)
        m0 = gallerys[top1]
        m1 = querys

        y_score = []
        # y_score = score(mat[ind, t1]).reshape(-1) + ((y_true == (gallerys[:, 1][top1] == querys[:, 1])) - 1) * 10
        score_max = mat[:, -1]
        y_score = np.array(score_max.reshape(-1))
        Predict_True = np.sum(gallerys[:, 1][top1] == querys[:, 1])
        y_true = gallerys[:, 1][top1] == querys[:, 1]

        # firstvalue=np.searchsorted(fpr,0,side="right")
        # milli_1 = np.searchsorted(fpr, 1e-4)
        # milli_1 = np.searchsorted(tpr, 0.915)
        # milli_1 = np.searchsorted(tpr,0.903)
        # thre = thresholds[milli_1]
        # print("thre: ", thre)
        print("gal's len", len(gallerys))
        # print("gallerys", gallerys)
        return y_true, y_score, mat, index, shape, np.array([]), np.array([])

    features = readFeatures(filename, len(labels))
    Query = features[query]
    Gallery = features[gallery]
    querys = labels[query]
    gallerys = labels[gallery]

    print "feature read!", datetime.datetime.now()

    D = cosine_similarity(Query, Gallery)

    MissedG = np.where(np.sum(Gallery * Gallery, axis=1) == 0)
    MissedQ = np.where(np.sum(Query * Query, axis=1) == 0)
    # print "missing Gallery",len(MissedG[0]),"Query",len(MissedQ[0])

    maxDist = 100
    D[:, MissedG] = maxDist
    D[MissedQ] = maxDist
    gallerys[MissedG] = -100
    # K = min(int(10 ** 6 / len(D)), len(D[0]) - 1)
    # K = min(int(10**8/len(D)), len(D[0])-1) #if 10e-8 is needed

    index = np.argpartition(D, -1)
    index_max = index[:, -1]
    # print "arg sorted",datetime.datetime.now()

    ind = np.arange(index.shape[0])[:, None]
    # score_max is last row of mat
    mat = D[ind, index]
    score_max = mat[:, -1]
    top1 = index_max.reshape(-1)
    y_score = np.array(score_max.reshape(-1))
    Predict_True = np.sum(gallerys[:, 1][top1] == querys[:, 1])
    y_true = gallerys[:, 1][top1] == querys[:, 1]
    print y_true

    y_true[MissedQ] = False
    shape = (len(query), len(gallery))
    saveData(y_true, y_score, rocfile, mat, index, shape)
    return y_true, y_score, mat, index, shape, features, top1


def plot_f(y_true, y_score, title, style, minx, lbfn, kind, recall_kind):
    global GroundTruth, Predict_True

    minx = minx
    pos_num = sum(GroundTruth == 1)
    neg_num = sum(GroundTruth == 0)
    pre_true_num = np.sum(Predict_True)
    print ("pos_num=", pos_num)
    print ("neg_num=", neg_num)
    print ("pre_true_num=", pre_true_num)
    num_points = int(sys.argv[4])
    y_score = np.array(y_score)

    # y_score = np.array([0.95, 0.90, 0.86, 0.75, 0.88, 0.80, 0.91, 0.85, 0.72, 0.80, 0.91, 0.98, 0.99, 0.87, 0.51, 0.5,])
    # y_true = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0])
    # y_score = np.array([0.1, 0.35, 0.4, 0.8])
    # y_true = np.array([0, 1, 0, 1])
    # y_true = y_true >= 0.5

    # min_y = -1
    min_y = y_score.min()
    max_y = y_score.max()
    print ("max_score=", max_y)
    print ("min_score=", min_y)
    step = 1.0 * (max_y - min_y) / num_points

    far = []
    recall = []
    Threshould = []
    for i in range(num_points):
        th = max_y - i * step
        Threshould.append(th)
        tmp = y_score >= th
        fp = tmp & (~ y_true)
        fn = (~tmp) & (y_true)
        tp = tmp & y_true
        tn = (~tmp) & (~y_true)
        # print ('fn =', fn.sum(), 'tp =', tp.sum(), 'fp =', fp.sum(), 'tn =', tn.sum())

        if fp.sum() == 0:
            far_ = 0
            # far.append(far_)
            continue
        else:
            far_ = 1.0 * fp.sum() / (fp.sum() + tp.sum())
            far.append(far_)

            if recall_kind == "1":
                recall_ = 1.0 * tp.sum() / GroundTruth.sum()
            else:
                recall_ = 1.0 * tp.sum() / y_true.sum()
            recall.append(recall_)

        print ("far=", far_, "recall=", recall_, "threshould=", th)

    if np.sum(GroundTruth) == 0:
        plt.plot(far, recall, 'r.')
    else:
        plt.plot(far, recall, style, label=title + " " + str(round(float(Predict_True) / np.sum(GroundTruth), 3)))

    # if Starting from the minimum of 'far' other than zero
    for f in far:
        if f != 0:
            min_far = f
            break

    for i in range(1, 8):
        b = -i
        t = 1 * 10 ** b
        if min_far < t:
            continue
        else:
            minx = t
            c = i
            break
    print minx

    find = minx
    minx = 1e-6
    # find = min(1e-4, minx)
    plt.xscale("log")
    plt.xlim([10 ** int(math.log(minx, 10) - 1), 1])
    # plt.xlim([find, 1])

    # plt.xlim([-0.01, maxfar])
    plt.ylim([-0.01, 1.01])
    plt.xlabel('FAR')
    plt.ylabel('RECALL')
    plt.title(getTitle(lbfn, kind))
    # plt.legend(loc='upper left')
    plt.legend(loc="best")
    plt.grid(True)

    for i in range(1, int(-math.log(find, 10))+1):
        a = find * (10 ** i)
        milli = np.searchsorted(far, a, side='left')
        try:
            rec = recall[milli]
        except:
            break
        thre = Threshould[milli]
        print int(-math.log(find, 10))
        print find * (10 ** i)
        plt.text(find * (10 ** i), rec-0.05, ("%.e" % (0.1**(c-i)), round(rec, 6)), ha='center', fontsize=6)
        plt.text(find * (10 ** i), rec-0.075, round(thre, 6), ha='center', fontsize=5)
        plt.scatter(find * (10 ** i), rec, c='k', marker='.')
    plt.savefig(getsavename(kind), dpi=200)
    plt.show()

    return 1e-3


def plot(y_true, y_score, title, style):
    global GroundTruth, Predict_True
    fpr, tpr, thresholds = roc_curve(y_true, y_score, pos_label=1, sample_weight=None, drop_intermediate=True)
    firstvalue = np.searchsorted(fpr, 0, side="right")
    milli = np.searchsorted(fpr, 1e-5)
    milli_1 = np.searchsorted(fpr, 1e-4)
    print title
    if tpr[firstvalue] < minStartThreshold:
        return 1
    if kind[0] == "1":
        print Predict_True, "/", np.sum(GroundTruth), "= %f" % (1.0 * Predict_True / np.sum(GroundTruth))
    plt.plot([fpr[firstvalue] / 10, fpr[firstvalue]], [tpr[firstvalue], tpr[firstvalue]], style)
    plt.plot(fpr, tpr, style, label=title + " " + str(round(float(Predict_True) / np.sum(GroundTruth), 3)))
    # a = raw_input("Continue")
    # print "1st error similarity =",thresholds[firstvalue]
    # print "1/1000 error similarity = ",thresholds[milli]
    print "1e-4 tpr = ", tpr[milli_1]
    print "1e-5 tpr = ", tpr[milli]
    return fpr[firstvalue]


def getTitle(lbfn, kind):
    key = lbfn.split("_")[-1]
    GName = {"xj": "xinjiang", "4w": "HQXJ_4w", "sc": "shangchao"}
    tname = GName[key] if GName.has_key(key) else key
    flag = "N" if kind == "1" else "1"
    title = tname + ' 1:' + flag
    return title


def getsavename(kind):
    name = "top1" if kind == "1" else "top250"
    suffix = 0
    while os.path.exists(name + "_" + str(suffix) + ".png"):
        suffix += 1
    savename = name + "_" + str(suffix) + ".png"
    return savename


def getStyle(cnt):
    color = ["r", "b", "g", "c", "y", "k", "m"]
    marker = ["o", "v", "s", "x", "+", "."]
    linestyle = ["", "--", ":"]
    return color[cnt % 7] + linestyle[cnt % 3]


def checkConsistency(query, gallery, D, index, shape):
    global GroundTruth, Predict_True
    if len(query) != shape[0] or len(gallery) != shape[1]:
        print "this label is not the same with npz record!"
        print "Delete old npz file if it is obsolete, or kind=-1 if choose to ignore"
        sys.exit()
    else:
        ind = np.arange(index.shape[0])[:, None]
        index = np.argpartition(D, -1)
        index_max = index[:, -1]
        top1 = index_max.reshape(-1)
        querys = labels[query]
        gallerys = labels[gallery]

        if kind[0] == "1":

            #            y_true= (gallerys[:,1][top1]==querys[:,1])
            #            y_score=score(mat[ind,t1].reshape(-1))
            # y_true = GroundTruth
            #            y_score=score(mat[ind,t1]).reshape(-1)*(y_true == (gallerys[:,1][top1]==querys[:,1]))
            # y_score = score(mat[ind, t1]).reshape(-1) + ((y_true == (gallerys[:, 1][top1] == querys[:, 1])) - 1) * 10
            y_score = []
            for i in range(len(index_max)):
                y_score.extend(D[ind[i], index_max[i]])
            y_score = np.array(y_score)

            PreT = gallerys[:, 1][top1] == querys[:, 1]
            y_true = PreT
            print PreT
            Predict_True = np.sum(gallerys[:, 1][top1] == querys[:, 1])
            print Predict_True

        else:
            y_true = (gallerys[:, 1][index].T == querys[:, 1]).T.reshape(-1)
            y_score = score(D.reshape(-1))
            Predict_True = np.sum(y_score)
        return top1, y_true, y_score


def DrawMerged(labels, query, gallery, mats, indexs, kind, cnt):
    size = len(mats)
    querys = labels[query]
    gallerys = labels[gallery]

    for i in xrange(size - 1):
        for j in xrange(i + 1, size):
            print i, j
            mat = np.concatenate(([mats[i]], [mats[j]]), axis=0)
            index = np.concatenate(([indexs[i]], [indexs[j]]), axis=0)
            y_true, y_score, top1 = plotMerge(mat, index, gallerys, querys, str(i) + ":" + str(j) + "Merged",
                                              getStyle(cnt), kind)
            cnt += 1

    if len(mats) > 2:
        y_true, y_score, top1 = plotMerge(mats, indexs, gallerys, querys, "all Merged", getStyle(cnt), kind)

    return y_true, y_score, top1


def plotMerge(mats, indexs, gabels, qlabels, name, style, kind):
    global GroundTruth
    m_true = []
    m_score = []
    mnum = len(mats)
    qnum = len(qlabels)
    gnum = len(gabels)
    S = sparse.csr_matrix((qnum, gnum))

    for i in range(mnum):
        S += sparse.csr_matrix((score(mats[i].reshape(-1)), (
            np.tile(np.arange(qnum).reshape(-1, 1), mats[i].shape[1]).reshape(-1), indexs[i].reshape(-1))),
                               shape=(qnum, gnum))
    argmin = S.argmax(1)
    top1 = np.array(argmin).reshape(-1)

    if kind[0] == "1":
        y_true = GroundTruth
        #        y_score=np.array(S[(np.arange(len(top1)),top1)]).reshape(-1)/mnum*(y_true == (gabels[:,1][top1]==qlabels[:,1]))
        #        y_score=score(mat[ind,t1]).reshape(-1)+(1-(y_true == (gallerys[:,1][top1]==querys[:,1])))*10
        y_score = np.array(S[(np.arange(len(top1)), top1)]).reshape(-1) / mnum + (
                (y_true == (gabels[:, 1][top1] == qlabels[:, 1])) - 1) * 10
    #        y_score=np.array(S[(np.arange(len(top1)),top1)]).reshape(-1)/mnum
    #        y_true= (gabels[:,1][top1]==qlabels[:,1])
    else:
        rows, cols = S.nonzero()
        y_score = np.array(S[(rows, cols)])[0] / mnum
        y_true = (gabels[:, 1][cols] == qlabels[:, 1][rows])

    plot(y_true, y_score, name, style)

    return y_true, y_score, top1


def plotMerge_bak(mats, indexs, gabels, qlabels, name, style, kind):
    m_true = []
    m_score = []
    mnum = len(mats)
    qnum = len(qlabels)
    gnum = len(gabels)

    for i in range(qnum):
        dic = {}
        for j in range(mnum):
            for k in range(gnum):
                index = indexs[j][i][k]
                dist = mats[j][i][k]
                dic[index] = [dic[index][0] + dist ** 2, dic[index][1] + 1] if dic.has_key(index) else [dist ** 2, 1]

        for key in dic:
            dic[key][0] += (len(mats) - dic[key][1]) * 1.5
        for key in dic:
            dic[key][1] = key

        value_list = sorted(list(dic.values()))
        m_true.append(Gallery_labels[int(value_list[0][1])] == Query_labels[i])
        m_score.append(-value_list[0][0])

    plot(m_true, m_score, name, style)
    return


if __name__ == '__main__':
    sys.argv = [__file__, '1',
                './puppy_testrec',
                './dpn_feats',
                '1000',
                '1'  # kind of recall: [if=0 ,recall=TP/(TP+FN);
                                      # if=1 ,recall=TP/(TP+FP+FN)]
                ]
    kind = sys.argv[1]  # "1" if only top1 "0" if all   "-1" is to show results on different label file on one
    labelfn = sys.argv[2]  # "groud truth file"
    num_point = sys.argv[4]
    recall_kind = sys.argv[-1]

    cnt = 0
    minx = 1e-3
    mats = []
    indexs = []

    labels, gallery, query = getlabels(labelfn)
    feats = np.empty((len(labels), 0), "f")
    tmp = ['resnet-se', 'custom']
    for i, file in enumerate(sys.argv[3:4]):
        y_true, y_score, mat, index, shape, features, top1 = getScores(file, labels, gallery, query, kind)
        min_ = plot_f(y_true, y_score, str(cnt) + ":" + tmp[i], getStyle(cnt), minx, labelfn, kind[0], recall_kind)
        minx = min(min_, minx)

        indexs.append(index)
        mats.append(mat)

        if PlotMerge and DrawWrong:
            feats = np.concatenate((feats, features), 1)

        cnt += 1
    # print y_score
    if len(mats) > 1 and PlotMerge and kind != "-1":
        y_true, y_score, top1 = DrawMerged(labels, query, gallery, mats, indexs, kind, cnt)
        features = feats

    if PrintTop1Pairs or DrawWrong:
        drawTop1(labels, query, gallery, y_true, y_score, features, top1, file)
