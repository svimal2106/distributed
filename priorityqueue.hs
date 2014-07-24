--priority queue implemetation

data Ord k => Priorityqueue k a = Null
                                | Node k a (Priorityqueue k a) (Priorityqueue k a) 
                                
--showqueue instance
instance (Ord k,Show k,Show a)=>Show (Priorityqueue k a) where
  show t = show' t
  
--show'::(Ord k,Show k,Show a)=>(Priorityqueue k a)->String
show' Null = "Null"
show' (Node p v lt rt) = "Node " ++ show p ++ " " ++ show v ++ " (" ++ (show' lt) ++ ") (" ++ (show' rt)++")"
--return an empty priority queue
empty::Ord k => Priorityqueue k a
empty = Null

--return a singleton priority queue
singleton::Ord k =>(k,a)->Priorityqueue k a
singleton (p,v) = Node p v Null Null

--inspect the minpriority element

inspectmin::Ord k => (Priorityqueue k a)->(k,a)
inspectmin Null = error "queue is empty"
inspectmin (Node p v _ _) = (p,v)

--extract the minpriority element
--extractmin::Ord k => (Priorityqueue k a)->(



--helper merge function
helpermerge::Ord k  => (Priorityqueue k a)->(Priorityqueue k a)->(Priorityqueue k a)
helpermerge (Node p v Null rt) t = Node p v t rt
helpermerge (Node p v lt rt) t = Node p v rt (merge t rt)

--merge function to merge two priority queues

merge::Ord k => (Priorityqueue k a)->(Priorityqueue k a)->(Priorityqueue k a)
merge l@(Node p1 v1 _ _) Null = l
merge Null r@(Node p2 v2 _ _) = r
merge l@(Node p1 v1 _ _) r@(Node p2 v2 _ _) | p1<=p2 = helpermerge l r
					    | otherwise = helpermerge r l
			    

--insert a (key,value) pair 

insert::Ord k =>(k,a)->(Priorityqueue k a)->(Priorityqueue k a)
insert (p,v) q = merge q (singleton (p,v))

import IO
main = do hdl <- openFile "test.txt" ReadMode
          echo hdl
echo hdl = do t <- hIsEOF hdl
              if t then return ()
                   else do x <- hGetChar hdl
                           putChar x
                           echo hdl
                     


