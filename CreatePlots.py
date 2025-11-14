
from math import sqrt
import sys
import os
import ROOT

src  = os.path.realpath("rootFiles__2016HIPM_v9/mkShapes__2016HIPM_v9.root") # root file to be used

normalise = True
plot = True

status = "work in progress"

method = "MoMEMta"
title = method+", 13.6 TeV, 27 PU"
Low = ""
cat  = "hww2l2v_13TeV_of2j_vbf" + Low # this must match the key in cuts dict in cuts.py (key in cuts dict + "_" + key of cut  )
var  = "kd_hpvbf_MMta" # this must match the key of the variable in variables.py
folder = method + "/"
var_unity = ""
prod = "qqH_hww" # this must match the key in samples.py
prod2 = "VBF_H0PH" # this must match the key in samples.py
prod3 = "VBF_H0M" # this must match the key in samples.py
prod4 = "VBF_H0L1" # this must match the key in samples.py
prod5 = "ggH_hww"
bkg = "WW" # this must match the key in samples.py

threshold = 9

discriminant = r"VBF(BSM)"  # subscript used in plot titles
#########################################

def setPlotParams(histo, colour):
    histo.SetLineColor(colour)
    histo.SetLineWidth(2)
    histo.SetMarkerColor(colour)
    histo.SetMarkerStyle(20)
    histo.SetMarkerSize(0.4)
    histo.SetFillColor(colour)
    histo.SetFillStyle(0)



def openAndPlotHisto(f, hstr, prodi, histo, canvas, legend, normalise=True, colour=ROOT.kBlack):
    if histo is None:
        histo = None
        if prodi != "":
            hstr = hstr.replace(prod, prodi)
            histo = f.Get(""+hstr+"")
            histo.SetDirectory(0)
    if canvas is not None and histo is not None:
        canvas.cd()
        setPlotParams(histo, colour)
        if (normalise):
            histo.Scale(1/histo.Integral())
        legend.AddEntry(histo, prodi, "l")
        histo.Draw("same HIST")
    return histo

f = ROOT.TFile.Open(''+src+'', 'read')
hstr = ''+cat+'/'+var+'/histo_'+prod
h1 = f.Get(""+hstr+"")
h1.SetDirectory(0)
h2 = openAndPlotHisto(f, hstr, prod2, None, None, None)
h3 = openAndPlotHisto(f, hstr, prod3, None, None, None)
h4 = openAndPlotHisto(f, hstr, prod4, None, None, None)
h5 = openAndPlotHisto(f, hstr, prod5, None, None, None)
hbkg = openAndPlotHisto(f, hstr, bkg, None, None, None)
f.Close()

def printEvents(histo, method, prod, threshold):
    print(f"\n{prod:-^{50}}")
    print("Total "+prod+" events:", histo.Integral())
    print("Greater than 0."+str(threshold)+" window "+prod+" events for "+method+":", histo.Integral(threshold, 10))

print(f"\n{discriminant+' discriminant ('+method+')':-^{100}}")

printEvents(h1, method, prod, threshold)
if hbkg is not None:
    printEvents(hbkg, method, bkg, threshold)
if h2 is not None:
    printEvents(h2, method, prod2, threshold)
if h3 is not None:
    printEvents(h3, method, prod3, threshold)
if hbkg is not None:
    print(f"\n{'Significance over '+discriminant+' bkg (D > 0.'+str(threshold)+')':-^{50}}")
    print("Significance for "+method+":", h1.Integral(threshold, 10) / sqrt(hbkg.Integral(threshold, 10)), "\n")


if plot:
    canvas = ROOT.TCanvas('canvas', '', 500, 500)
    ROOT.gStyle.SetOptStat(0)
    h1.SetTitle("")
    h1.GetXaxis().SetTitle(r"D_{"+discriminant+r"}"+" "+var_unity)
    legend = ROOT.TLegend(0.50, 0.65, 0.85, 0.85)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.035)
    legend.SetFillStyle(0)
    openAndPlotHisto(None, None, prod, h1, canvas, legend, normalise, ROOT.kBlack)
    openAndPlotHisto(None, None, prod2, h2, canvas, legend, normalise, ROOT.kRed)
    openAndPlotHisto(None, None, prod3, h3, canvas, legend, normalise, ROOT.kMagenta)
    openAndPlotHisto(None, None, prod4, h4, canvas, legend, normalise, ROOT.kOrange-3)
    openAndPlotHisto(None, None, prod5, h5, canvas, legend, normalise, ROOT.kBlue)
    openAndPlotHisto(None, None, bkg, hbkg, canvas, legend, normalise, 8)
    h1.GetYaxis().SetRangeUser(0., 1.) # only if needed
    h1.GetXaxis().SetRangeUser(0., 1.)
    legend.Draw("same")

    # if h2 is not None:
    #     setPlotParams(h2, ROOT.kRed)
    # if h3 is not None:
    #     setPlotParams(h3, ROOT.kBlue)
    # if hbkg is not None:
    #     setPlotParams(hbkg, 8)

    # if (Low == "L"):
    #     h1.SetTitle(r"D_{"+discriminant+r"}"+" including low-energy jets"+" ("+method+")")
    # else:
    #     h1.SetTitle(r"D_{"+discriminant+r"}"+" ("+method+")")
    # if (normalise):
    #     h1.GetYaxis().SetTitle('Events normalised to 1')
    #     h1.Scale(1/h1.Integral())
    #     if h2 is not None:
    #         h2.Scale(1/h2.Integral())
    #     if h3 is not None:
    #         h3.Scale(1/h3.Integral())
    #     if hbkg is not None:
    #         hbkg.Scale(1/hbkg.Integral())
    # h1.Scale(1/h1.GetMaximum())
    #     h2.Scale(1/h2.GetMaximum())
    #     hbkg.Scale(1/hbkg.GetMaximum())
    # else:
    #     h1.GetYaxis().SetTitle('Events')
    #     h1tot = h1.Integral()
    #     h2tot = 0
    #     h3tot = 0
    #     hbkgtot = 0
    #     if h2 is not None:
    #         h2tot = h2.Integral()
    #     if h3 is not None:
    #         h3tot = h3.Integral()
    #     if hbkg is not None:
    #         hbkgtot = hbkg.Integral()
    #     maximums = [h1tot, h2tot, h3tot, hbkgtot]
    #     h1.Scale(max(maximums))
    # h1.Draw("")
    # h2.Draw("same")
    # hbkg.Draw("same")
    # h1.Draw("HIST")
    # if h2 is not None:
    #     h2.Draw("same HIST")
    # if h3 is not None:
    #     h3.Draw("same HIST")
    # if hbkg is not None:
    #     hbkg.Draw("same HIST") # only if needed

    firsttex = ROOT.TLatex()
    firsttex.SetTextSize(0.03)
    firsttex.DrawLatexNDC(0.02,0.91,"#scale[1.5]{       CMS} " + status)
    firsttex.Draw("same")

    secondtext = ROOT.TLatex()
    secondtext.SetTextSize(0.035)
    secondtext.SetTextAlign(31)
    secondtext.DrawLatexNDC(0.90, 0.91, title)
    secondtext.Draw("same")

    if not os.path.exists("plots/"):
        os.makedirs("plots/")
    if not os.path.exists("plots/pdfs/"):
        os.makedirs("plots/pdfs/")
    if not os.path.exists("plots/pngs/"):
        os.makedirs("plots/pngs/")
    if not os.path.exists("plots/root/"):
        os.makedirs("plots/root/")

    if not os.path.exists("plots/pdfs/"+folder):
        os.makedirs("plots/pdfs/"+folder)
    if not os.path.exists("plots/pngs/"+folder):
        os.makedirs("plots/pngs/"+folder)
    if not os.path.exists("plots/root/"+folder):
        os.makedirs("plots/root/"+folder)

    prods = prod+"_"+prod2+"_"+prod3+"_"+prod4+"_"+prod5
    canvas.SaveAs("plots/pdfs/"+folder+cat+"_"+var+"_"+prods+"_"+bkg+"_"+method+".pdf")
    canvas.SaveAs("plots/pngs/"+folder+cat+"_"+var+"_"+prods+"_"+bkg+"_"+method+".png")
    canvas.SaveAs("plots/root/"+folder+cat+"_"+var+"_"+prods+"_"+bkg+"_"+method+".root")
