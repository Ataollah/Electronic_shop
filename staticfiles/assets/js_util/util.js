export const PASSWORD_PATTERN = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$/;

export const formatPrice = (price, language) => {
    const isEnglish = language === 'en';
    const formattedPrice = price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return isEnglish ? `$${formattedPrice}` : `${formattedPrice} ریال`;
  };




export const formatPriceWithSeparator = (price) => {
  return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};



