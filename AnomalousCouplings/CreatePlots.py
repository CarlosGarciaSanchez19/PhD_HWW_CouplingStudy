
from math import sqrt
import sys
import os
import ROOT

src  = os.path.realpath("rootFiles__2016HIPM_v9/mkShapes__2016HIPM_v9_VBFCPeven_h_MoMEMta.root")

normalise = True
plot = True

status = "work in progress"
title = "13.6 TeV, 27 PU"

method = "MoMEMta"
Low = ""
cat  = "hww2l2v_13TeV_of2j_vbf" + Low
var  = "D_0CPeven_h"
folder = method + "/"
var_unity = ""
prod = "qqH_hww"
prod2 = ""
bkg = "VBF_H0PH"

discriminant = r"0^{+}_{h}"

########

def open_histos(src, cat, var, prod, prod2, bkg):
    h1 = None
    h2 = None
    hbkg = None
    if bkg == "":
        bkg = None
    if prod2 == "":
        prod2 = None
    f = ROOT.TFile.Open(''+src+'', 'read')
    hstr = ''+cat+'/'+var+'/histo_'+prod
    h1 = f.Get(""+hstr+"")
    h1.SetDirectory(0)
    if prod2 is not None:
        h2 = f.Get(hstr.replace('qqH_hww', prod2))
        h2.SetDirectory(0)
    hstr = ''+cat+'/'+var+'/histo_'+bkg
    if bkg is not None:
        hbkg = f.Get(""+hstr+"")
        hbkg.SetDirectory(0)
    f.Close()
    return h1, h2, hbkg

h1, h2, hbkg = open_histos(src, cat, var, prod, prod2, bkg)

print(f"\n{discriminant+' discriminant ('+method+')':-^{100}}")

print(f"\n{prod:-^{50}}")
print("Total "+prod+" events:", h1.Integral())
print("Greater than 0.8 window "+prod+" events for "+method+":", h1.Integral(9, 10))
if hbkg is not None:
    print(f"\n{bkg:-^{50}}")
    print("Total "+bkg+" events:", hbkg.Integral())
    print("Greater than 0.8 window "+bkg+" events for "+method+":", hbkg.Integral(9, 10))
if h2 is not None:
    print(f"\n{prod2:-^{50}}")
    print("Total "+prod2+" events:", h2.Integral())
    print("Greater than 0.8 window "+prod2+" events for "+method+":", h2.Integral(9, 10))
if hbkg is not None:
    print(f"\n{'Significance over '+discriminant+' bkg (D > 0.8)':-^{50}}")
    print("Significance for "+method+":", hbkg.Integral(9, 10) / sqrt(h1.Integral(9, 10)), "\n")

if plot:
    canvas = ROOT.TCanvas('canvas', '', 500, 500)
    ROOT.gStyle.SetOptStat(0)
    h1.SetLineColor(ROOT.kBlack)
    h1.SetLineWidth(2)
    h1.SetMarkerColor(ROOT.kBlack)
    h1.SetMarkerStyle(20)
    h1.SetMarkerSize(0.4)
    h1.SetFillColor(ROOT.kBlack)
    h1.SetFillStyle(0)
    if h2 is not None:
        h2.SetLineColor(ROOT.kRed)
        h2.SetLineWidth(2)
        h2.SetMarkerColor(ROOT.kRed)
        h2.SetMarkerStyle(20)
        h2.SetMarkerSize(0.4)
        h2.SetFillColor(ROOT.kRed)
        h2.SetFillStyle(0)

    # if (Low == "L"):
    #     h1.SetTitle(r"D_{"+discriminant+r"}"+" including low-energy jets"+" ("+method+")")
    # else:
    #     h1.SetTitle(r"D_{"+discriminant+r"}"+" ("+method+")")
    h1.SetTitle("")
    h1.GetXaxis().SetTitle(r"D_{"+discriminant+r"}"+" "+var_unity)
    h1.GetYaxis().SetTitle('Events normalised to 1')
    if (normalise):
        h1.Scale(1/h1.Integral())
        if h2 is not None:
            h2.Scale(1/h2.Integral())
        if hbkg is not None:
            hbkg.Scale(1/hbkg.Integral())
    # h1.Scale(1/h1.GetMaximum())
    #     h2.Scale(1/h2.GetMaximum())
    #     hbkg.Scale(1/hbkg.GetMaximum())
    elif hbkg is not None:
        h1.Scale(hbkg.Integral())
    if hbkg is not None:
        hbkg.SetLineColor(ROOT.kBlue)
        hbkg.SetLineWidth(2)
        hbkg.SetMarkerColor(ROOT.kBlue)
        hbkg.SetFillColor(ROOT.kBlue)
        hbkg.SetFillStyle(0)
        hbkg.SetMarkerStyle(20)
        hbkg.SetMarkerSize(0.4)
    # h1.Draw("")
    # h2.Draw("same")
    # hbkg.Draw("same")
    h1.Draw("HIST")
    if h2 is not None:
        h2.Draw("same HIST")
    if hbkg is not None:
        hbkg.Draw("same HIST")
    h1.GetYaxis().SetRangeUser(.0, .8) # only if needed
    h1.GetXaxis().SetRangeUser(0., 1.) # only if needed

    firsttex = ROOT.TLatex()
    firsttex.SetTextSize(0.03)
    firsttex.DrawLatexNDC(0.02,0.91,"#scale[1.5]{       CMS} " + status)
    firsttex.Draw("same");

    secondtext = ROOT.TLatex()
    secondtext.SetTextSize(0.035)
    secondtext.SetTextAlign(31)
    secondtext.DrawLatexNDC(0.90, 0.91, title)
    secondtext.Draw("same")

    legend = ROOT.TLegend(0.50, 0.65, 0.85, 0.85)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.035)
    legend.SetFillStyle(0)
    legend.AddEntry(h1, prod, "l")
    if h2 is not None:
        legend.AddEntry(h2, prod2, "l")
    if hbkg is not None:
        legend.AddEntry(hbkg, bkg, "l")
    legend.Draw("same")
    canvas.SaveAs("plots/pdfs/"+folder+cat+"_"+var+"_"+prod+"_with_"+bkg+"bkg_"+method+"_test.pdf")
    canvas.SaveAs("plots/pngs/"+folder+cat+"_"+var+"_"+prod+"_with_"+bkg+"bkg_"+method+"_test.png")

