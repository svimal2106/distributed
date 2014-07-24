import IO
main = do hdl <- openFile "test.txt" ReadMode
          echo hdl
echo hdl = do t <- hIsEOF hdl
              if t then return ()
                   else do x <- hGetChar hdl
                           putChar x
                           echo hdl
                     