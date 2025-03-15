import Foundation

class CodeAnalysisViewModel: ObservableObject {
    @Published var results: String = ""

    func analyzeCode(_ code: String) {
        // Call PythonScriptRunner to run the analysis
        PythonScriptRunner.runScript(code) { output in
            DispatchQueue.main.async {
                self.results = output
            }
        }
    }
}