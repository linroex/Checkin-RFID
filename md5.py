from hashlib import md5
file = open("/Users/linroex/Project/md5_generate/num.txt")
nums = file.read().split("\n")
for num in nums:
    h = md5()
    h.update(num.encode("utf8"))
    print(h.hexdigest())