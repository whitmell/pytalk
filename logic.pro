tc_search(K,Word,Rels,Sent):-
  distinct(Id,
    (tc(K,Word,Rels,_RelatedWord,res(_Steps,Ids,_Path)),
     member(Id,Ids)
    )
  ),
  nice_sent(Id,Sent).

tc(K,A,Rels,B,res(Steps,Ids,Path)):-
  distinct(A+B+End,tc(A,Rels,B,[],_AnyIds,K,End,res(N,Ids,RevPath))),
  Steps is K-N,
  reverse(RevPath,Path).


tc(A,Rels,C,Xs,Ids1,SN1,N2,Res) :-
  succ(N1,SN1),
  member(Rel,Rels),
  call_svo(A,Rel,B,Ids2),
  not(memberchk(B-_,Xs)),
  reconcile(Ids1,Ids2,Ids3),
  tc1(B,Rels,C,[A-Rel|Xs],Ids3,N1,N2,Res).

tc1(B,_Rels,B,Xs,Ids,N,N,res(N,Ids,Xs)).
tc1(B,Rels,C,Xs,Ids,N1,N2,Res) :-
   tc(B,Rels,C,Xs,Ids,N1,N2,Res).

reconcile(Ids1,Ids,Ids2):-var(Ids1),!,Ids2=Ids.
reconcile(Ids1,Ids,Ids2):-intersection(Ids1,Ids,Ids2),Ids2=[_|_].

call_svo(A,Rel,B,Ids):-svo(A,Rel,B,Ids);svo(B,Rel,A,Ids).

nice_sent(N,Sent):-
  sent(N,Ws),
  intersperse([N,':'|Ws],' ',SWs),
  atomic_list_concat(SWs,Sent).

% intersperses words Ws with separator X
intersperse(Ws,X,Ys):-intersperse(Ws,X,Ys,[]).

intersperse([],_)-->[].
intersperse([W|Ws],X)-->[W,X],intersperse(Ws,X).

intersperse0(Ws,X,Ys0):-intersperse(Ws,X,Ys),once(append(Ys0,[_],Ys)).

do(Gs):-call(Gs),fail;true.

ppp(X):-writeln('DEBUG'=X).


%%%%%%%%%%%%

:-ensure_loaded('examples/tesla.pro').

/*

a--r->b
|f    |g
v     v
c--r->d

*/

analogy_via(F,[A:T,R,B:T,as,C:S,R,D:S]):-
  svo(A,R,B,RAB),
  svo(C,R,D,RCD),
  intersection(RAB,RCD,[_|_]),
  
  svo(A,F,B,FAB),
  svo(C,F,D,FCD),
  
  intersection(FAB,FCD,[_|_]),
   
   
  svo(A,U,T,UAT),
  svo(B,U,T,UBT),
  svo(C,V,S,UCS),
  svo(D,V,S,UDS),
  
  sort([A,B,C,D,S,T],[_,_,_,_,_,_]),
  append([RAB,RCD,FAB,FCD,UAT,UBT,UCS,UDS],All),
  sort(All,Sorted),
  length(Sorted,Len),
  Len<12,
  true.

similar(A,B):-
  svo(T,R,A,Ids1),
  svo(T,R,B,Ids2),
  A@<B,
  svo(A,RR,S,Ids3),
  svo(B,RR,S,Ids4),
  intersection(Ids1,Ids2,[_|_]),
  intersection(Ids3,Ids4,[_|_]).


go:-do((
  tc(2,law,[is_a,part_of,contains,is_like,as_in],A,Res),
  writeln(A+Res)
)).

go1:-do((
  analogy_via(F,A),writeln(F:A)
)).


go2:-do((
  tc_search(3,'gun',[_,_],R),
  ppp(R)
)).

go3:-
 do((
   similar(A,B),
   writeln([A,is,similar,to,B])
 )).
