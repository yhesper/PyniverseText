(* input: Graph: (int map) arr, edge list: (int * int) arr, temp_map: array *)
(* output: Simplical Elimination ordering: int list, temp_map: string to int map *)

(* an seo: (str hashtbl, str * int array) *)
open! Core
module ST = String.Table
module S = Strint.Set


let search graph = 
    let (adj, _) = graph in (* adj is a (str, str list) hash table *)
    let n = ST.length adj in
    let str2idx_tbl = ST.create () in 
    let idx2str_arr = Array.create ~len:n "" in
    let vertices = ST.keys adj in
    let v_arr = List.to_array vertices in
    for i = 0 to n-1 do
        print_string(Array.get v_arr i);
        print_endline(" ");
    done;
    let weights_tbl = ST.create () in
    let weights_tree_ref : Strint.Set.t ref = ref (List.fold vertices ~init:(S.empty) 
                                    ~f:(fun tree v -> print_string(v);(if (S.mem tree (v, 0)) then print_endline("wtf") else print_endline("??"))
                                    ;(ST.add_exn weights_tbl ~key:v ~data:0)
                                    ;(S.add tree (v, 0)))) in
    
    print_string("current tree size is");
    print_string(Int.to_string(Set.length (!weights_tree_ref)));
    print_endline(".");

    
    for i = 0 to (n-1) do
        let weights_tree = !weights_tree_ref in
        let (v, w_v)= S.max_elt_exn weights_tree in
        let nbhrs : string list = ST.find_exn adj v in
        let update_weight (tree: S.t) (u: string) = 
                (match (ST.find weights_tbl u) with
                | Some(w_u) -> begin
                                    let tmp_tree = S.remove tree (u, w_u) in
                                    S.add tmp_tree  (u, w_u+1)
                               end
                | None -> tree)
        in
        let weights_tree = List.fold nbhrs ~init:weights_tree ~f:update_weight in
        (* remove v from weights table and weights tree*)
        let weights_tree = S.remove weights_tree (v, w_v) in
        weights_tree_ref := weights_tree;
        (ST.remove weights_tbl v);
        (* update the ordering table and array *)
        (ST.add_exn str2idx_tbl ~key:v ~data:i);
        (Array.set idx2str_arr i v);
    done;
    (str2idx_tbl, idx2str_arr)
;;

let print (_, arr) = 
    let msg = ref "printing the simplicial elim ordering: " in
    let n = Array.length arr in
    for i = 0 to (n-1) do 
        msg := (!msg) ^ (Array.get arr i) ^ " | "
    done;
    !msg
;;

(* some expect tests *)
let%expect_test "Test parsing of an empty program:" =
  let g = ST.create () in
  ST.add_exn g ~key:"t1" ~data:["x"];
  ST.add_exn g ~key:"t2" ~data:["x"];
  ST.add_exn g ~key:"t3" ~data:["x"];
  ST.add_exn g ~key:"t4" ~data:["x";"z"];
  ST.add_exn g ~key:"t5" ~data:["x";"z"];
  ST.add_exn g ~key:"x" ~data:["t1";"t2";"t3";"t4";"t5"];
  ST.add_exn g ~key:"y" ~data:["x";"z";"t4"];
  ST.add_exn g ~key:"z" ~data:["x";"y";"t4";"t5"];
  let f = Edge.Table.create () in 
  let graph = (g, f) in
  print_endline (print (search graph));
  [%expect
    {| ??? |}]
;;