//
//  AnalysisResultView.swift
//  Neurasense
//
//  Created by ARYAN SEHRAWAT on 1/14/25.
//


import SwiftUI

struct AnalysisResultView: View {
    var results: String

    var body: some View {
        ScrollView {
            Text(results)
                .foregroundColor(.white)
                .padding()
        }
        .background(Color.darkGray)
        .cornerRadius(10)
        .padding()
    }
}