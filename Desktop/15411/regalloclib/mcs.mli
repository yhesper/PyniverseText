open! Core

val search : string list String.Table.t * unit Edge.Table.t -> int String.Table.t * string array
val print : int String.Table.t * string array -> string