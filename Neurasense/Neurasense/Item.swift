//
//  Item.swift
//  Neurasense
//
//  Created by ARYAN SEHRAWAT on 1/12/25.
//

import Foundation
import SwiftData

@Model
final class Item {
    var timestamp: Date
    
    init(timestamp: Date) {
        self.timestamp = timestamp
    }
}
