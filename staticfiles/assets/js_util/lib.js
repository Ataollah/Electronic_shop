 const toEnglishNumber = (strNum) => {
            let pn = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"];
            let en = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];

            let cache = strNum;
            for (let i = 0; i < 10; i++) {
                let regex_fa = new RegExp(pn[i], 'g');
                cache = cache.replace(regex_fa, en[i]);
            }
             return cache;
    }

 const isUsernameEmailOrPhone = (username) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^09\d{9}$/;

    return phoneRegex.test(username) || emailRegex.test(username); ;
}